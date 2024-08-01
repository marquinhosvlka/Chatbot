import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:uuid/uuid.dart';
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart';  // Importa o pacote mime

class ChatProvider extends ChangeNotifier {
  final List<types.Message> _messages = [];
  List<types.Message> get messages => _messages;

  final types.User _user = types.User(id: 'user');

  final types.User _bot = types.User(
    id: 'bot',
    firstName: 'Bot',
    imageUrl: 'https://cdn-icons-png.flaticon.com/512/6014/6014401.png',
  );

  void addMessage(types.Message message) {
    _messages.insert(0, message);
    notifyListeners();
  }

  Future<void> sendMessage(String content) async {
    final message = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: Uuid().v4(),
      text: content,
    );

    addMessage(message);

    try {
      final response = await http.post(
        Uri.parse('https://apitensorflow-hb6ixpzc6q-rj.a.run.app/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': content}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final botMessage = types.TextMessage(
          author: _bot,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: Uuid().v4(),
          text: data['response'],
        );
        addMessage(botMessage);
      } else {
        addMessage(types.TextMessage(
          author: _bot,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: Uuid().v4(),
          text: 'Erro ao obter resposta',
        ));
      }
    } catch (e) {
      addMessage(types.TextMessage(
        author: _bot,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: Uuid().v4(),
        text: 'Erro de conexão',
      ));
    }
  }

  Future<void> sendImage(File imageFile) async {
    final message = types.ImageMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: Uuid().v4(),
      name: imageFile.path.split('/').last,
      size: await imageFile.length(),
      uri: imageFile.path,
      width: 1440,
      height: 1440, // ajuste conforme necessário
    );

    addMessage(message);

    // Determina o MIME type da imagem
    final mimeType = lookupMimeType(imageFile.path) ?? 'image/jpg'; // Define um MIME type padrão caso não seja encontrado

    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('https://apitensorflow-hb6ixpzc6q-rj.a.run.app/analyze_emotion'),
      );

      request.files.add(
        http.MultipartFile.fromBytes(
          'image',
          await imageFile.readAsBytes(),
          filename: imageFile.path.split('/').last,
          contentType: MediaType.parse(mimeType),
        ),
      );

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = jsonDecode(responseBody);
        final botMessage = types.TextMessage(
          author: _bot,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: Uuid().v4(),
          text: data['dominant_emotion'],
        );
        addMessage(botMessage);
      } else {
        addMessage(types.TextMessage(
          author: _bot,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: Uuid().v4(),
          text: 'Erro ao processar imagem',
        ));
      }
    } catch (e) {
      addMessage(types.TextMessage(
        author: _bot,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: Uuid().v4(),
        text: 'Erro de conexão',
      ));
    }
  }
}
