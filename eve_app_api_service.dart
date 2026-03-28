import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseURL = 'http://127.0.0.1:8000/api';
  
  static Future<String> sendMessage(String content, {String model = 'mistral'}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseURL/chat'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'content': content,
          'model': model,
        }),
      ).timeout(Duration(seconds: 60));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['response'];
      } else {
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      return 'Error: $e';
    }
  }

  static Future<List<Map>> getHistory({int limit = 50}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseURL/history?limit=$limit'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<Map>.from(data['messages']);
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  static Future<bool> checkModelStatus() async {
    try {
      final response = await http.get(
        Uri.parse('$baseURL/model/status'),
      ).timeout(Duration(seconds: 2));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['running'] == true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  static Future<bool> ensureModelRunning() async {
    try {
      final response = await http.post(
        Uri.parse('$baseURL/model/ensure-running'),
      ).timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['success'] == true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
}
