import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:uuid/uuid.dart';

class ChatProvider extends ChangeNotifier {
  final List<types.Message> _messages = [];
  List<types.Message> get messages => _messages;

  // Defina o usuário sem avatar
  final types.User _user = types.User(id: 'user');

  
  final types.User _bot = types.User(
    id: 'bot',
    firstName: 'Bot',
    imageUrl: 'https://cdn-icons-png.flaticon.com/512/6014/6014401.png',
  );

  Future<void> sendMessage(String content) async {
    final message = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: Uuid().v4(),
      text: content,
    );

    _messages.insert(0, message);
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('https://chatbot-a1ca.onrender.com/ask'),
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
        _messages.insert(0, botMessage);
      } else {
        _messages.insert(0, types.TextMessage(
          author: _bot,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: Uuid().v4(),
          text: 'Erro ao obter resposta',
        ));
      }
    } catch (e) {
      _messages.insert(0, types.TextMessage(
        author: _bot,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: Uuid().v4(),
        text: 'Erro de conexão',
      ));
    }

    notifyListeners();
  }
}
