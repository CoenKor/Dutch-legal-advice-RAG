import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.prompts.prompt import PromptTemplate
from llm import llm, embeddings
from langchain.chains import RetrievalQA

# this code initializes a Neo4jVector retriever using an existing index 
# defines a prompt for question-answering (QA)
# sets up a retrieval-based QA system with a LLM
neo4jvector = Neo4jVector.from_existing_index(
    embedding = embeddings,                             
    url=st.secrets["NEO4J_URI"],             
    username=st.secrets["NEO4J_USERNAME"],   
    password=st.secrets["NEO4J_PASSWORD"],   
    index_name="casePlots",                  
    node_label="ecli",                       
    text_node_property="beslissing",       
    embedding_node_property="embedding",     
    retrieval_query="""
RETURN
    node.beslissing AS text,
    score,
    {
        source: node.ECLI,
        bewijzen: [(node)-[:bevat]->(bewezenverklaring) | bewezenverklaring.data ]
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

QA_PROMPT = """
Question: Mijn cliënt heeft de volgende tenlastelegging: 2 Tenlastelegging Verdachte wordt, kort gezegd, beschuldigd van:  Feit 1: medeplegen van handel in cocaïne en heroïne in de periode van 26 december 2018 tot en met 22 februari 2021 te Amsterdam;  Feit 2: (eenvoudig) (schuld)witwassen van een geldbedrag van € 2.296,05 op 22 februari 2021 te Amsterdam. De volledige tekst van de tenlastelegging is opgenomen in bijlage I.
Context:[{{"text": '9 Beslissing De rechtbank komt op grond van het voorgaande tot de volgende beslissing. Verklaart het onder 1 ten laste gelegde niet bewezen en spreekt verdachte daarvan vrij. Verklaart bewezen dat verdachte het onder 2 ten laste gelegde heeft begaan zoals hiervoor in rubriek 4 is vermeld. Verklaart niet bewezen wat aan verdachte meer of anders is ten laste gelegd dan hiervoor is bewezen verklaard en spreekt verdachte daarvan vrij. Het bewezen verklaarde levert op: ten aanzien van feit 2: opzettelijk handelen in strijd met het in artikel 2 onder C van de Opiumwet gegeven verbod. Verklaart het bewezene strafbaar. Verklaart verdachte, [verdachte], daarvoor strafbaar. Veroordeelt verdachte tot een gevangenisstraf van 35 (vijfendertig) maanden. Beveelt dat de tijd die door veroordeelde voor de tenuitvoerlegging van deze uitspraak in verzekering en in voorlopige hechtenis is doorgebracht, bij de tenuitvoerlegging van die straf in mindering gebracht zal worden. Verklaart verbeurd: 5 1 STK Tas (Omschrijving: Sporttas 5992715). Dit vonnis is gewezen door mr. F. Dekkers, voorzitter, mrs. C.P. Bleeker en A.F. Bazdidi Tehrani, rechters, in tegenwoordigheid van L. Jaakke-van den Berg, griffier, en uitgesproken op de openbare terechtzitting van deze rechtbank van 18 februari 2021.'}}, {{"source": 'ECLI:NL:RBAMS:2021:6669'}}, {{"bewijzen":'4 Bewezenverklaring De rechtbank acht bewezen dat verdachte:  Zaak A: op 17 september 2020 te Amsterdam, op de openbare weg [straatnaam] , met het oogmerk van wederrechtelijke toeëigening heeft weggenomen een tasje (onder meer inhoudende een Nederlands paspoort en een Syrisch paspoort en twee telefoons en een  oplader), toebehorende aan [slachtoffer] , welke diefstal werd vergezeld en gevolgd van geweld tegen voornoemde [slachtoffer] , gepleegd met het oogmerk om die diefstal gemakkelijk te maken en/of om het bezit van het gestolene te verzekeren, welk geweld hierin bestond, dat hij, verdachte - met kracht dat tasje uit de handen van voornoemde [slachtoffer] heeft getrokken en - met een mes, in de linkerarm en het linkerbeen en de hand van die [slachtoffer] heeft gestoken en/of gesneden.'}}]
Helpful Answer: Ik kom op grond van het voorgaande tot de volgende beslissing. Verklaart het onder 1 ten laste gelegde niet bewezen en spreekt verdachte daarvan vrij. Verklaart bewezen dat verdachte het onder 2 ten laste gelegde heeft begaan zoals hiervoor in rubriek 4 is vermeld. Verklaart niet bewezen wat aan verdachte meer of anders is ten laste gelegd dan hiervoor is bewezen verklaard en spreekt verdachte daarvan vrij. Het bewezen verklaarde levert op: ten aanzien van feit 2: (eenvoudig) (schuld)witwassen van een geldbedrag van € 2.296,05. Verklaart het bewezene strafbaar. Verklaart verdachte, [naam van de verdachte], daarvoor strafbaar. Veroordeelt verdachte tot een gevangenisstraf van 2 maanden. Beveelt dat de tijd die door veroordeelde voor de tenuitvoerlegging van deze uitspraak in verzekering en in voorlopige hechtenis is doorgebracht, bij de tenuitvoerlegging van die straf in mindering gebracht zal worden. Verklaart verbeurd: 1 STK Tas (Omschrijving: Sporttas 5992715).


Follow this example when generating answers.


It can also be the case that the provided information is empty. In this case, give the verdict based on your own knowlegde about the Dutch Legal System. Be clear when you are using your own knowledge instead of using the provided context!

Information:
{context}

Question: {question}
Helpful Answer:
"""

qa_prompt = PromptTemplate.from_template(QA_PROMPT)

kg_qa = RetrievalQA.from_chain_type(
    llm,                 
    chain_type="stuff",
    verbose=True,       
    chain_type_kwargs={"prompt": qa_prompt},
    retriever=retriever,  
)