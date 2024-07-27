// lib/models/message.dart
class Message {
  final String role; // 'user' ou 'bot'
  final String content;

  Message({required this.role, required this.content});
}
