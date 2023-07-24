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

# AI promt
template = """You are an AI whose work is to know the name and reason of the caller and provide these details to admin. But if the caller seems to be a scammer or very suspicious,
ai have to warn admin about the risk, along with the name and reason of the caller. The conversation between the caller and AI is given in the following array [{previous_chat}].
Ai should continues the conversation by outputting a single sentence. AI will not ask to much details of reason."""

# Initialize language chain
prompt = PromptTemplate(input_variables=["previous_chat"], template=template)
chatgpt_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)


@app.route('/api/myendpoint', methods=['POST'])
def my_endpoint():
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
