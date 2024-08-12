

# OncoKnowledge

OncoKnowledge is a Flutter application designed to provide quick answers about cancer using a backend API hosted on Google Cloud Run. The backend is built with Flask and utilizes the Gemini API to generate responses based on a text file containing relevant information about cancer.

## Overview

The Flutter app uses the `flutter_chat_ui` library to create a user-friendly chat interface. When a user asks a question, the app sends a POST request to the backend API hosted on Google Cloud Run. The API processes the question and the content of the text file to generate an appropriate response.

## Functionality

- **User Query**: The user types a question into the app's chat interface.
- **Request to API**: The app makes a POST request to the API hosted on Google Cloud Run.
- **Processing the Query**: The API uses the Gemini API to generate a response based on the content of the text file.
- **Response**: If the response is found in the content, Gemini generates it. If not, Gemini provides an evasive response, which is then adjusted by the system to better fit the chatbot's intended reply.

## Requirements

- Flutter SDK
- Python 3.x
- Flask
- `google.generativeai` library
- `flutter_chat_ui` library

## Project Structure

1. **Flutter Application**:
    - Uses the `flutter_chat_ui` library to create the chat interface.
    - Sends POST requests to the API using the `http` library.

2. **Flask Backend**:
    - File: `app.py`
    - Configured to use the Gemini API to generate responses based on a text file.
    - Hosted on Google Cloud Run.

## How to Run the Project

### Flask Backend

1. **Set Up Environment**:
    - Install dependencies:
      ```bash
      pip install flask google-generativeai
      ```

2. **Configuration File**:
    - Create a file named `content.txt` in the same directory as `app.py` and add the relevant content about cancer.

3. **Start Flask Server**:
    - Run the Flask app:
      ```bash
      python app.py
      ```

4. **Deploy to Google Cloud Run**:
    - Follow instructions to set up and deploy the service to Google Cloud Run.

### Flutter Application

1. **Set Up Environment**:
    - Make sure you have the Flutter SDK installed.

2. **Install Dependencies**:
    - In the Flutter project directory, run:
      ```bash
      flutter pub get
      ```

3. **Run the Application**:
    - Start the Flutter app:
      ```bash
      flutter run
      ```

## Customization

- **Change Content**: To create informational chatbots on other topics, edit the content in the `content.txt` file.
- **Adjust Responses**: Modify the code in `app.py` to adjust how evasive responses are handled and adapted.

## Contributing

If you want to contribute to the project, feel free to open an issue or submit a pull request.
