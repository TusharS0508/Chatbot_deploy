import os
import requests
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class HuggingFaceModelProcessor:
    def __init__(self, api_key=None):
        self.client = InferenceClient(
            provider="novita",
            api_key=api_key or os.getenv("HF_TOKEN")
        )
        self.model_name = "meta-llama/Llama-3.1-8B-Instruct"

    def query_huggingface(self, messages):
        """Call Hugging Face Inference API"""
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return completion
        except Exception as e:
            print(f"API Error: {e}")
            return {"choices": [{"message": {"content": "Sorry, I couldn't process that request."}}]}

    def generate_response(self, prompt, conversation_history=None, system_message=None, use_api=True):
        """Generate response"""
        if use_api:
            messages = []
            
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            if conversation_history:
                messages.extend([
                    msg for msg in conversation_history 
                    if msg["role"] != "system"
                ])
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            try:
                response = self.query_huggingface(messages)
                if hasattr(response, "choices") and len(response.choices) > 0:
                    return response.choices[0].message.content
                return "Sorry, I couldn't process your request. Please try again."
            except Exception as e:
                print(f"API Error: {e}")
                return "Sorry, I couldn't process your request. Please try again."
        else:
            return "Local model not implemented - using API instead"