import streamlit as st
from rag_chatbot import Chatbot

def is_valid_api_key(api_key):
    """Test if the key works with a lightweight Hugging Face API call."""
    try:
        test_url = "https://huggingface.co/api/whoami-v2"
        response = requests.get(
            test_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
        return response.status_code == 200
    except:
        return False


def main():
    st.title("Competitive Programming Assistant")
    
    api_key = st.text_input("Enter Hugging Face API Key", type="password")
    api_key = api_key.strip()
    if api_key and not is_valid_api_key(api_key):
        st.error("Invalid API key. Please check and try again.")
        st.stop()

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
