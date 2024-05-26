from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory 
from llm import llm
from langchain.prompts import PromptTemplate
from tools.vector import kg_qa

# enabling chat history for the last 5 prompts
memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True,
)

# making the tools to use for the LLM
# a general chat where it is just ChatGPT or vector search in the Neo4j graph database
tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat not covered by other tools",
        func=llm.invoke,
        return_direct=False
        ),
    Tool.from_function(
        name="Vector Search Index",  
        description="Uses Vector Search to search for similar case indictments", 
        func = kg_qa, 
        return_direct=False
    ),
]

# system prompt
agent_prompt = PromptTemplate.from_template("""
ALWAYS use 'Vector Search Index' tool
                                            
Use the recieved context to create a verdict for the given case indictment of the user.
What you basically have to do, is creating a verdict (that normally a judge would give) for the given indictment based on the context you get (which is context from an earlier, similar case).
The context contains the verdict from a judge and other information used in a similar case.
Also use your own reasoning in the creation of your answer by interpreting the given context.

It can also be the case that the provided information is empty or that the provided information doesn't align with the particular indictment of the user. In this case, you have to give a verdict (where you give the punishment and severity of the punishment) based on your own knowlegde about the Dutch Legal System. 

Be clear to the user if you are using just your own knowledge OR using the provided context! Be clear by stating this in your output.                        

Give your answer in the most organized structure possible.
                                            
Give every answer in the Dutch language!
                                            
For every verdict that you predict (with provided knowledge or your own knowledge), you have to give the type of punishment and the severity of each punishment that you give. Except for an acquittal, then it is just acquittal.

SO ALSO GIVE THE PUNISHMENT WHEN USING YOUR OWN KNOWLEDGE                                    
TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# function for a handler that calls the conversational agent and returns a response
def generate_response(prompt):
    response = agent_executor.invoke({"input": prompt})

    return response['output']


