import requests
import os
from dotenv import load_dotenv

load_dotenv()

class HuggingFaceModelProcessor:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("HE_API_KEY")
        print(f"API Key Status: {'Provided' if self.api_key else 'Missing'}")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model_name = "accounts/fireworks/models/llama-v3p1-8b-instruct"

    def query_huggingface(self, messages):
        """Call Hugging Face Inference API for Llama 3.1 8B Instruct"""
        payload = {
            "messages": messages,
            "model": self.model_name,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return {"choices": [{"message": {"content": "Sorry, I couldn't process that request."}}]}

    def generate_response(self, prompt, use_api=True):
        """Generate response using Hugging Face API with chat format"""
        if use_api:
            messages = [{
                "role": "user",
                "content": prompt
            }]
            
            try:
                response = self.query_huggingface(messages)
                if "choices" in response and len(response["choices"]) > 0:
                    return response["choices"][0]["message"]["content"]
                return "Sorry, I couldn't process your request. Please try again."
            except Exception as e:
                print(f"API Error: {e}")
                return "Sorry, I couldn't process your request. Please try again."
        else:
            return "Local model not implemented - using API instead"
