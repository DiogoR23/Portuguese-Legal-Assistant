from flask import Flask, request, jsonify
from ai_assistant.chatbot import main as chatbot

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot_endpoint():
    data = request.json
    user_message = data.get('message', "")
    response = chatbot(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)