from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from rag_chatbot import Chatbot
import os

app = FastAPI()

bot = Chatbot()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>CP Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chatbox { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #userInput { width: 70%; padding: 8px; }
        button { padding: 8px 15px; }
        .user { color: blue; margin: 5px 0; }
        .bot { color: green; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Competitive Programming Assistant</h1>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="Type your question...">
    <button onclick="sendMessage()">Send</button>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value;
            input.value = '';
            
            // Add user message
            document.getElementById('chatbox').innerHTML += 
                `<div class="user"><strong>You:</strong> ${message}</div>`;
            
            // Get bot response
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            
            // Add bot response
            document.getElementById('chatbox').innerHTML += 
                `<div class="bot"><strong>Bot:</strong> ${data.response}</div>`;
            
            // Scroll to bottom
            document.getElementById('chatbox').scrollTop = 
                document.getElementById('chatbox').scrollHeight;
        }
        
        // Allow pressing Enter to send
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    response = bot.respond(data["message"])
    return {"response": response}