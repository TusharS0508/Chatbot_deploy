import streamlit as st
from rag_chatbot import Chatbot
from model_processor import HuggingFaceModelProcessor

def main():
    st.title("Competitive Programming Assistant")
    st.write("Ask questions about programming problems or provide a problem ID (e.g., 2093I) to get started.")
    
    # Initialize API key variable
    api_key = None
    
    # Try to get API key from secrets if available
    try:
        if hasattr(st, 'secrets') and 'HF_TOKEN' in st.secrets:
            api_key = st.secrets.HF_TOKEN
            st.sidebar.success("Using API key from secrets")
    except Exception:
        pass  # Silently ignore if secrets aren't available
    
    # If no API key from secrets, show input field
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
        # Create model processor with the API key
        model_processor = HuggingFaceModelProcessor(api_key=api_key)
        # Initialize chatbot with the model processor
        chatbot = Chatbot()
        chatbot.model = model_processor
        return chatbot
    
    # Initialize chatbot with the API key
    bot = load_chatbot(api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.spinner("Thinking..."):
            response = bot.respond(prompt)
    
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()