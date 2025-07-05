import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

class HuggingFaceModelProcessor:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")  # Key from .env
        self.api_url = "https://api-inference.huggingface.co/models/accounts/fireworks/models/llama-v3p1-8b-instruct"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def query_huggingface(self, messages):
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": messages[0]["content"]},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return {"error": str(e)}
