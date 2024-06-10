# Thesis Project: Integrating RAG Models in the Dutch Legal System

Welcome to the GitHub page for the thesis of Coen Korevaar (13441728). This project focuses on creating a Retrieval-Augmented Generation (RAG) model to answer the following question: 

**To what extent can a Retrieval-Augmented Generation (RAG) model be integrated in the creation of verdicts in the Dutch legal system?**

The dataset used for this project is `parsed_data.csv`.

## Setting Up the Model

To set up the model, follow these steps:

1. **Install Dependencies**:
   - Install the required libraries listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up a Neo4J Graph**:
   - Create an account on Neo4J and choose 'AuraDB FREE' to create your first knowledge graph.
   - Import your CSV into the knowledge graph, specifying your entities and relationships.

3. **Generate Embeddings**:
   - Use the `Embedding.ipynb` notebook to generate embeddings for every indictment in the dataset. This is essential for enabling vector search in Neo4J.
   - The embeddings are generated using OpenAI's `text-embedding-3-small` model.
   - Integrate the resulting CSV from the notebook into the Neo4J database by adding a new property to all indictment nodes in the graph.

4. **Integrate Embeddings in Graph Database**:
   - Publish the CSV by using the 'share with the internet' function in Google Drive.
   - Generate a shareable link for the CSV, then run the following query in the terminal of your Neo4J database:
     ```cypher
     LOAD CSV WITH HEADERS
     FROM 'LINK_HERE'
     AS row
     MATCH (ecli:ecli {ECLI: row.ECLI})
     CALL db.create.setNodeVectorProperty(ecli, 'embedding', apoc.convert.fromJsonList(row.embeddings))
     RETURN count(*)
     ```

5. **Create a Vector Index**:
   - Create a vector index by running the following query in the terminal of your Neo4J database:
     ```cypher
     CREATE VECTOR INDEX NAME_OF_YOUR_VECTOR_INDEX IF NOT EXISTS
     FOR (ecli:ecli)
     ON ecli.embedding
     OPTIONS {indexConfig: {
       `vector.dimensions`: 1536,
       `vector.similarity_function`: 'cosine'
     }}
     ```
   - Update the specific vector index name in the `vector.py` file located in the 'tools' folder to connect your vector index.
   - Specify the information you want to retrieve from the database.

6. **Run the Application**:
   - Import your Neo4J credentials (username, connection, and password) and your OpenAI credentials (API key and model name) into a file named `secrets.toml` in a folder called `.streamlit`.
   - Start the application using the `streamlit run` command:
     ```bash
     streamlit run bot.py
     ```
   - The app will be available at [http://localhost:8501/](http://localhost:8501/).

## Results

The results of this project are organized into several folders:

1. **RAG-model-Quality**:
   - Contains the input and output prompts of the model.
   - Includes prompts for similar cases (cases that are similar to those in the Neo4J database) and non-similar cases (cases that are not similar to those in the Neo4J database).

    **End Results**:
      - An Excel file comparing the verdicts created by the RAG model to the actual verdicts from `rechtspraak.nl`.

3. **Robustness**:
   - Contains 50 outputs of the model from the same case description to test robustness.
   - The code used for the calculation of robustness results can be found in `Robustness.ipynb` in the same folder.
