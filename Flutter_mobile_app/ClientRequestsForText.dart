import 'dart:convert';
import 'dart:io';


 //Uri uri = Uri(port: 8000, host: "localhost", scheme: "http",path: "/api");

void getrequest() async {
var client = HttpClient();
 final uri = Uri.parse('http://localhost:8000/');
  try {
    // создаем запрос
    HttpClientRequest request = await client.getUrl(uri);
    // получаем ответ
    HttpClientResponse response = await request.close();
    // обрабатываем ответ
    final stringData = await response.transform(utf8.decoder).join();
    print(stringData);
  } finally {
    client.close();
  }

}


// //клиентская часть с гетзапросом





void postrequst(var b) async {

  final client = HttpClient();

  try {
   
    final uri = Uri.parse('http://localhost:8000/');
    final req = await client.postUrl(uri);
    req.headers.set(HttpHeaders.contentTypeHeader, "application/json");
    req.headers.set(HttpHeaders.accessControlAllowOriginHeader, "*");
    req.headers.set(HttpHeaders.accessControlAllowHeadersHeader, "Content-Type");
     req.headers.set(HttpHeaders.refererHeader,"no-referrer-when-downgrade");
     req.headers.set(HttpHeaders.acceptEncodingHeader, "*");
    var a =json.encode({'title': b});
    req.write(a);
    //print(a);

    final response = await req.close();
    final responseBody = await response.transform(utf8.decoder).join();

    print('Статус код: ${response.statusCode}');
    print('Ответ от сервера: $responseBody');
  } finally {
    client.close();
  }
}











Future<void>  main() async {

 final filePath = '4.jpg'; // Замените на путь к вашему файлу
  convertFileToBytecode(filePath);
}

void convertFileToBytecode(String filePath) async {
  try {
    final file = File(filePath);
    final bytes = await file.readAsBytes();
     postrequst(bytes);
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
   // getrequest();
    
    
  } catch (e) {
    print('Ошибка при конвертации файла в байтовый код: $e');
  }

}