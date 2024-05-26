import streamlit as st
from utils import write_message
from llm import llm, embeddings
from graph import graph
from agent import generate_response

# this is the page config
st.set_page_config("Ebert", page_icon=":movie_camera:")

# setting up the session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey ik ben een Chatbot voor rechtsadvies!  Hoe kan ik je helpen?"},
    ]

# function for the submit handler
def handle_submit(message):
    # handle the response
    with st.spinner('Thinking...'):
        response = generate_response(message)
        write_message('assistant', response)

# displaying the messages in session state
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

# handling the user input
if prompt := st.chat_input("What is up?"):
    # displaying the user message in chat message container
    write_message('user', prompt)

    # generating a response
    handle_submit(prompt)
