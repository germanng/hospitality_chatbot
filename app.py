import streamlit as st
import re
from main import get_response

def clean_response(response):
    """Clean and format the chatbot response."""
    
    # Clean unwanted characters while retaining ".", ",", "!", and "/"
    cleaned = re.sub(r'[^a-zA-Z0-9.,!?/ ]', '', response)
    
    # Ensure spacing after punctuation marks
    cleaned = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', cleaned)
    
    # Remove extra spaces
    cleaned = ' '.join(cleaned.split())
    
    # Capitalize the first letter of each sentence after a sentence terminator followed by a space
    cleaned = re.sub(r'(?<=[.!?] )([a-z])', lambda x: x.group(1).upper(), cleaned)
    
    # Capitalize the first letter of the response, if it's a letter and the response doesn't start with a space
    if cleaned and cleaned[0].isalpha():
        cleaned = cleaned[0].upper() + cleaned[1:]
    
    # Add a period at the end if the last character is not a sentence terminator
    if cleaned and not cleaned[-1] in '.!?':
        cleaned += '.'
    
    return cleaned

# App Framework
st.title("🦜️🔗 Hotelier Assistant")

st.markdown("""
<style>
    .chat-message {
        font-family: Arial, sans-serif;
        white-space: normal !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if not hasattr(st.session_state, 'messages'):
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type in your message"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get chatbot's response
    response = get_response(prompt, chat_history=[])
    response = clean_response(response)  # Clean and format the response before displaying

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
