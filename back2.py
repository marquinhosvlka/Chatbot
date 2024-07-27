from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class PTSM:
    ISO_639_1 = "pt_core_news_sm"

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Crie o chatbot e treine-o com o corpus de dados
chatbot = ChatBot('CancerBot', tagger_language=PTSM)
trainer = ChatterBotCorpusTrainer(chatbot)

# Treine o chatbot com o corpus de câncer
trainer.train('cancer.yml')  # Substitua pelo caminho real do arquivo YAML

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    response = chatbot.get_response(question)
    return jsonify({'response': str(response)})

if __name__ == '__main__':
    app.run(debug=True)
