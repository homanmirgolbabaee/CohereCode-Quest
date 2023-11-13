import streamlit as st
from weaviate import Client as WeaviateClient
from weaviate.auth import AuthApiKey
import cohere
import numpy as np
from transformers import pipeline

def main():
    with st.sidebar:
        option = st.radio("Settings", ("🔧Weaviate", "🦜️Langchain", "🌏Multi-Lingual Chatbot"))

    if option == "🔧Weaviate":
        st.write("Weaviate Settings and Information")  # Replace with actual Weaviate content

    if option == "🦜️Langchain":
        st.write("Langchain Settings and Information")  # Replace with actual Langchain content

    if option == "🌏Multi-Lingual Chatbot":
        st.empty()
        print("CHATBOT")
        show_chatbot()
        

def show_chatbot():
    st.title("Advanced Chatbot")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    prompt = st.chat_input("Type your message...")
    if prompt:
        # Display user message and add to chat history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Placeholder for response generation logic
        response = "Placeholder response from the model"

        # Display the model's response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add model response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
if __name__ == "__main__":
    main()
