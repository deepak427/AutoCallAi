from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from langchain import OpenAI, LLMChain, PromptTemplate

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
open_ai_api_key = os.getenv("OPENAI_API_KEY")

# AI promte

template ="""[Context: You are an AI designed to assist the admin by handling caller information. Your primary task is to collect the caller's name and reason for contacting the admin. However, you also have to be vigilant for potential scammers or suspicious individuals.]

AI: Hello, I am the AI assistant here to help you. Please provide me with the name and reason of the caller.

Caller: [Caller provides their name and reason for contacting the admin.]

AI: Thank you for sharing the information. If the caller seems legitimate, I will relay their details to the admin for further assistance.

AI: However, if I detect any signs of potential scam or suspicious activity, I will promptly notify the admin about the risk, along with the name and reason provided by the caller.

AI: To maintain security, I will not ask for extensive details about the reason. Please keep your responses concise.

The most important points to always foolow is,
when responding: ai will always say the exact sentence "goodby, admin will contact you soon. exit" after knowing details of caller. .

[Admin's instructions: When responding, make sure to provide a single sentence continuation of the conversation based on the context and previous_chat provided in the JSON array.]

'previous_chat' array:
{previous_chat}
"""

# Initialize language chain
prompt = PromptTemplate(input_variables=["previous_chat"], template=template)
chatgpt_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)

@app.route('/', methods=['GET'])
def ai():
    try:
        result = {'message': "Welcome to Spam-Jam"}
        return jsonify(result), 200
    except Exception as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 400

@app.route('/api/aiResponse', methods=['POST'])
def ai_response():
    try:
        data = request.get_json()
        previous_chat = data.get('previous', "")
        if not previous_chat:
            raise ValueError("The 'previous' field is required in the request JSON.")

        output = chatgpt_chain.predict(previous_chat=previous_chat)
        result = {'message': output}
        return jsonify(result), 200
    except Exception as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5126)
