from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Defina o caminho para o diretório onde as imagens serão armazenadas
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Carregar o modelo pré-treinado (ajuste conforme o seu modelo)
model = tf.keras.models.load_model('path/to/your/model.h5')

# Função para processar a imagem e prever a emoção
def predict_emotion(image_path):
    # Abra a imagem e prepare-a para o modelo
    image = Image.open(image_path).resize((224, 224))  # Ajuste o tamanho conforme necessário
    image_array = np.array(image) / 255.0  # Normalizar a imagem
    image_array = np.expand_dims(image_array, axis=0)  # Adicionar dimensão de batch

    # Realizar a previsão
    predictions = model.predict(image_array)
    emotion = np.argmax(predictions[0])  # Obtenha a emoção com a maior probabilidade
    emotions = ['happy', 'sad', 'neutral', 'angry']  # Ajuste conforme as emoções do seu modelo

    return emotions[emotion]

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Prever a emoção
        emotion = predict_emotion(file_path)
        return jsonify({'dominant_emotion': emotion})

    return jsonify({'error': 'File processing error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
