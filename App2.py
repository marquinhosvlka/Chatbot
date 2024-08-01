from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from fer import FER
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Função para processar a imagem e prever a emoção
def predict_emotion(image_path):
    try:
        # Carregar a imagem
        img = cv2.imread(image_path)

        # Criar o detector de emoções
        detector = FER()

        # Detectar emoções
        result = detector.detect_emotions(img)

        if result:
            dominant_emotion = max(result[0]['emotions'], key=result[0]['emotions'].get)
            return dominant_emotion
        else:
            return 'unknown'
    except Exception as e:
        return f'Error during prediction: {str(e)}'

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

        try:
            # Prever a emoção
            emotion = predict_emotion(file_path)
            return jsonify({'dominant_emotion': emotion})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File processing error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
