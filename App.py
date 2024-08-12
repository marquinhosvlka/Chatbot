import os
from flask import Flask, request, jsonify
import logging
import google.generativeai as genai

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configure the Gemini API
GOOGLE_API_KEY = 'API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_gemini_response(question, content):
    prompt = (
        f"You are a virtual assistant specialized in providing information about cancer. "
        f"Answer the following question based on the information provided in the content below, "
        f"without mentioning the source of the information. If the answer is not available, say that you do not have the information. "
        f"Avoid using phrases like 'according to the text' or 'mentioned'. "
        f"Respond in a human-like and clear manner. The question is: '{question}'.\n\n"
        f"Content:\n{content}\n"
        f"Answer:"
        f"Whenever there is no answer, start with 'Sorry' or 'Apologies'. "
        f"Remember that the word 'you' should only refer to the person asking the question and never to the chatbot developer. "
        f"Never repeat the question to provide an answer, but if there are multiple {question}, answer all of them. "
        f"Never repeat phrases like 'the following types of cancer are mentioned:' or 'are mentioned in the content:' or 'mentioned are:'. Always speak in the first person, e.g., instead of saying mentioned, say 'I have the following information regarding your question'. "
        f"Understand that you are a chatbot, and thus the answer is yours and not from texts or contents."
        f"Never, ever use the word 'content'."
    )
    
    input_data = {'text': prompt}
    response = model.generate_content(input_data)
    
    answer = response.candidates[0].content.parts[0].text.strip()
    
    # Check if the answer contains unwanted terms
    unwanted_terms = ['I don’t know', 'I didn’t find', 'I suggest', 'refer to', 'sorry', 'apologies']
    if any(term in answer.lower() for term in unwanted_terms):
        return "Sorry, I don't have enough information to answer that question."

    return answer

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    try:
        # Load the content from the file
        with open('content.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return jsonify({'error': 'Content file not found'}), 500

    answer = generate_gemini_response(question, content)
    return jsonify({'response': answer})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
