import streamlit as st
from rag_chatbot import Chatbot

def main():
    st.title("Competitive Programming Assistant")
    
    # Add API key input (sidebar or main area)
    api_key = st.text_input(
        "Enter your Hugging Face API Key",
        type="password",  # Mask the key
        help="Get your key from https://huggingface.co/settings/tokens"
    )
    
    if not api_key:
        st.warning("Please enter your API key to continue.")
        return  # Stop execution if no key
    bot = Chatbot(api_key=api_key)  # Update Chatbot class to accept this

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Thinking..."):
            response = bot.respond(prompt)  # Pass API key if needed
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
