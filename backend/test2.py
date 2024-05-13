from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4
from urllib.parse import quote_plus

openai.api_key = "sk-proj-ulcP3hqe7zORRs3HwzT5T3BlbkFJXZVLLvjCU7hBU7Kafppo"

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes

# Setup MongoDB connection
# connStr = "mongodb://localhost:27017/" #Adding Atlas Connection
# Setup MongoDB connection
username = quote_plus('shreytalreja25')
password = quote_plus('Shrey@9999')
connStr = f"mongodb+srv://{username}:{password}@cluster0.3vb27rr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
client = MongoClient(connStr)  # Update with your MongoDB URI
db = client.unsw_chats
chats = db.chats

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['prompt']
    session_id = request.json.get('session_id', str(uuid4()))
    response = chat_with_gpt(user_input)

    # Check if session already exists
    existing_session = chats.find_one({"session_id": session_id})

    if existing_session:
        # Append the new messages to the existing session
        chats.update_one(
            {"session_id": session_id},
            {"$push": {"messages": [{"role": "user", "content": user_input}, {"role": "bot", "content": response}]}}
        )
    else:
        # Create a new session if it does not exist
        chats.insert_one({
            "session_id": session_id,
            "timestamp": datetime.utcnow(),
            "messages": [
                {"role": "user", "content": user_input},
                {"role": "bot", "content": response}
            ]
        })

    return jsonify({"response": response, "session_id": session_id})

def chat_with_gpt(prompt):
    modified_prompt = f"Answer as a UNSW assistant: {prompt}. Do not generate any response that is not related to UNSW."
    response = openai.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:unswbot:9Nm4NnHU",
        messages=[{"role":"user","content":modified_prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    app.run(debug=True)
