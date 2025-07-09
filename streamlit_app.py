import streamlit as st
from rag_chatbot import Chatbot
from model_processor import HuggingFaceModelProcessor

def main():
    st.title("Competitive Programming Assistant")
    st.write("Ask questions about programming problems or provide a problem ID (e.g., 2093I) to get started.")
    
    api_key = None
    
    try:
        if hasattr(st, 'secrets') and 'HF_TOKEN' in st.secrets:
            api_key = st.secrets.HF_TOKEN
            st.sidebar.success("Using API key from secrets")
    except Exception:
        pass
    
    if not api_key:
        api_key = st.sidebar.text_input(
            "Enter your Hugging Face API key:",
            type="password",
            help="Get your API key from Hugging Face"
        )
        
        if not api_key:
            st.warning("Please enter your Hugging Face API key to continue")
            st.stop()
        else:
            st.sidebar.success("Using provided API key")

    @st.cache_resource
    def load_chatbot(api_key):
        chatbot = Chatbot(api_key=api_key)
        return chatbot
    
    bot = load_chatbot(api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "system",
            "content": "You are a helpful competitive programming assistant."
        })

    for message in st.session_state.messages:
        if message["role"] != "system":  
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.spinner("Thinking..."):
            conversation_history = [
                msg for msg in st.session_state.messages 
                if msg["role"] in ["user", "assistant"]
            ]
            
            response = bot.respond(
                prompt,
                conversation_history=conversation_history,
                system_message="You are a competitive programming assistant."
            )
    
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})