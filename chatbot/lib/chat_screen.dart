import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'chat_provider.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'package:uuid/uuid.dart';
import 'dart:io';

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
        scrollPhysics: BouncingScrollPhysics(),
        showUserAvatars: true,
        showUserNames: true,
        onAttachmentPressed: () {
          _handleAttachmentPressed(context, chatProvider);
        },
      ),
    );
  }

  void _handleAttachmentPressed(BuildContext context, ChatProvider chatProvider) {
    showModalBottomSheet<void>(
      context: context,
      builder: (BuildContext context) => SafeArea(
        child: SizedBox(
          height: 192,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  _handleImageSelection(context, chatProvider);
                },
                child: const Align(
                  alignment: AlignmentDirectional.centerStart,
                  child: Text('Imagem da Galeria'),
                ),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  _handleCameraSelection(context, chatProvider);
                },
                child: const Align(
                  alignment: AlignmentDirectional.centerStart,
                  child: Text('Tirar Foto'),
                ),
              ),
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Align(
                  alignment: AlignmentDirectional.centerStart,
                  child: Text('Fechar'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _handleImageSelection(BuildContext context, ChatProvider chatProvider) async {
    final result = await ImagePicker().pickImage(
      imageQuality: 70,
      maxWidth: 1440,
      source: ImageSource.gallery,
    );

    if (result != null) {
      final imageFile = File(result.path);

      // Enviar a imagem para a API e adicionar a mensagem somente após o retorno da API
      await chatProvider.sendImage(imageFile);
    }
  }

  void _handleCameraSelection(BuildContext context, ChatProvider chatProvider) async {
    final result = await ImagePicker().pickImage(
      imageQuality: 70,
      maxWidth: 1440,
      source: ImageSource.camera,
    );

    if (result != null) {
      final imageFile = File(result.path);

      // Enviar a imagem para a API e adicionar a mensagem somente após o retorno da API
      await chatProvider.sendImage(imageFile);
    }
  }

  void _handleFileSelection(ChatProvider chatProvider) async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.any,
    );

    if (result != null && result.files.single.path != null) {
      final message = types.FileMessage(
        author: types.User(id: 'user'),
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: Uuid().v4(),
        mimeType: result.files.single.extension,
        name: result.files.single.name,
        size: result.files.single.size,
        uri: result.files.single.path!,
      );

      chatProvider.addMessage(message);
    }
  }
}
