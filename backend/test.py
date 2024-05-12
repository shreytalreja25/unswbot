from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

openai.api_key = "sk-proj-ulcP3hqe7zORRs3HwzT5T3BlbkFJXZVLLvjCU7hBU7Kafppo"

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains on all routes

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['prompt']
    response = chat_with_gpt(user_input)
    return jsonify({"response": response})

def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:unswbot:9Nm4NnHU",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    app.run(debug=True)
