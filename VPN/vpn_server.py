import socket
import threading
from cryptography.fernet import Fernet
from datetime import datetime

# Генерируем симметричный ключ для шифрования
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Конфигурация сервера
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5555

def handle_client(client_socket, addr):
    """Обработка клиентского соединения"""
    print(f"[{datetime.now()}] [+] Клиент подключился: {addr}")
    try:
        while True:
            data = client_socket.recv(65536)
            if not data:
                print(f"[{datetime.now()}] [!] Клиент {addr} отключился")
                break
                
            # Дешифрование сообщения
            try:
                decrypted = cipher.decrypt(data).decode()
                print(f"[{datetime.now()}] [↓] Получено {len(data)} байт | Расшифровано: {decrypted[:100]}{'...' if len(decrypted) > 100 else ''}")
            except Exception as e:
                print(f"[{datetime.now()}] [!] Ошибка дешифрования: {str(e)}")
                continue
            
            # Формирование ответа
            response = f"[Сервер] Принято {len(decrypted)} симв. в {datetime.now().strftime('%H:%M:%S')}"
            encrypted_response = cipher.encrypt(response.encode())
            
            # Отправка ответа
            client_socket.sendall(encrypted_response)
            print(f"[{datetime.now()}] [↑] Ответ отправлен ({len(encrypted_response)} байт)")
            
    except Exception as e:
        print(f"[{datetime.now()}] [!] Ошибка: {str(e)}")
    finally:
        client_socket.close()

def main():
    # Выводим ключ для использования в клиенте
    print(f"[{datetime.now()}] [*] Сгенерирован симметричный ключ:")
    print(f"[{datetime.now()}] [*] KEY = {KEY.decode()}")
    print(f"[{datetime.now()}] [*] (Скопируйте эту строку в клиентский скрипт)")
    
    # Запуск сервера
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[{datetime.now()}] [*] Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    
    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()
            print(f"[{datetime.now()}] [*] Активных подключений: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] [!] Сервер остановлен")
    finally:
        server.close()

if __name__ == "__main__":
    main()