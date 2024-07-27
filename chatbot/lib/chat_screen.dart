import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'chat_provider.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;

class ChatScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final chatProvider = Provider.of<ChatProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Chatbot'),
      ),
      body: Chat(
        messages: chatProvider.messages,
        onSendPressed: (types.PartialText message) {
          chatProvider.sendMessage(message.text);
        },
        user: types.User(id: 'user'),
        scrollPhysics: BouncingScrollPhysics(), // Adiciona o efeito de rolagem
        showUserAvatars: true, // Mostra os avatares dos usuários
        showUserNames: true, // Mostra os nomes dos usuários
      ),
    );
  }
}
