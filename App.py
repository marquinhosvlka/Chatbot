from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

questions = [
    "O que é câncer?",
    "Quais são os tipos de câncer mais comuns?",
    "Quais são os sintomas do câncer de mama?",
    "Quais são os sintomas do câncer de pulmão?",
    "Quais são os sintomas do câncer de próstata?",
    "Quais são os sintomas do câncer de cólon?",
    "Quais são os fatores de risco para câncer?",
    "Como é feito o diagnóstico de câncer?",
    "Quais são os tratamentos disponíveis para câncer?",
    "Como a quimioterapia trata o câncer?",
    "Como a radioterapia trata o câncer?",
    "O que é imunoterapia?",
    "O que são terapias alvo?",
    "Como prevenir o câncer?",
    "Qual a importância do diagnóstico precoce do câncer?",
    "boa noite"
]

answers = [
    "Câncer é uma doença caracterizada pelo crescimento descontrolado de células anormais no corpo.",
    "Os tipos de câncer mais comuns incluem câncer de mama, pulmão, próstata e cólon.",
    "Os sintomas do câncer de mama podem incluir um caroço na mama, mudanças no tamanho ou forma da mama, e secreção pelo mamilo.",
    "Os sintomas do câncer de pulmão podem incluir tosse persistente, dor no peito, falta de ar e perda de peso inexplicável.",
    "Os sintomas do câncer de próstata podem incluir dificuldade para urinar, fluxo urinário fraco, sangue na urina e dor pélvica.",
    "Os sintomas do câncer de cólon podem incluir mudanças nos hábitos intestinais, sangue nas fezes, dor abdominal e perda de peso inexplicável.",
    "Fatores de risco para câncer incluem tabagismo, exposição a radiação, dieta pobre, falta de atividade física e predisposição genética.",
    "O diagnóstico de câncer pode ser feito através de exames como biópsias, tomografias, ressonâncias magnéticas e exames de sangue.",
    "Os tratamentos para câncer incluem cirurgia, radioterapia, quimioterapia, imunoterapia e terapias alvo.",
    "A quimioterapia trata o câncer usando medicamentos que matam células cancerosas ou impedem seu crescimento.",
    "A radioterapia usa radiação de alta energia para matar células cancerosas ou impedir seu crescimento.",
    "A imunoterapia estimula o sistema imunológico do corpo para combater o câncer.",
    "Terapias alvo são tratamentos que atacam especificamente as células cancerosas sem afetar muito as células normais.",
    "Para prevenir o câncer, recomenda-se evitar o tabagismo, manter uma dieta saudável, praticar atividade física regular, e fazer exames regulares de rastreamento.",
    "O diagnóstico precoce do câncer é importante porque aumenta as chances de sucesso do tratamento e pode salvar vidas.",
    "Boa noite, tudo bem?"
]

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(questions).toarray()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    question_vector = vectorizer.transform([question]).toarray()
    similarity = cosine_similarity(question_vector, vectors)
    index = np.argmax(similarity)
    response = answers[index]
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
