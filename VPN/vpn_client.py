import socket
import requests
from cryptography.fernet import Fernet
from datetime import datetime

# Конфигурация
SERVER_IP = "127.0.0.1"  # Замените на реальный IP сервера
SERVER_PORT = 5555

# Вставить ключ, что и на сервере!
KEY_STR = "pJDMSB0fPUIrR-3qAmFQvESNUhfnziHrpaLUMjcsMss="  # Замените на ключ из вывода сервера
KEY = KEY_STR.encode()
cipher = Fernet(KEY)

def connect_to_server():
    """Установка соединения с сервером"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    print(f"[{datetime.now()}] [+] Подключено к серверу {SERVER_IP}:{SERVER_PORT}")
    return client

def main():
    client = connect_to_server()
    
    try:
        while True:
            print("\n" + "="*50)
            print("Выберите действие:")
            print("1. Отправить текстовое сообщение")
            print("2. Отправить HTML с example.com")
            print("3. Проверить ping")
            print("4. Выход")
            choice = input(">>> ")
            
            if choice == "1":
                message = input("Введите сообщение: ").strip()
                if not message:
                    continue
                data = message.encode()
            elif choice == "2":
                print(f"[{datetime.now()}] [*] Загрузка HTML с example.com...")
                response = requests.get("http://example.com")
                data = response.content
                print(f"[{datetime.now()}] [*] Загружено {len(data)} байт")
            elif choice == "3":
                data = b"PING_REQUEST"
                start_time = datetime.now()
                print(f"[{datetime.now()}] [*] Отправка ping...")
            elif choice == "4":
                print(f"[{datetime.now()}] [*] Отключение...")
                break
            else:
                print("[!] Неверный выбор")
                continue
                
            # Шифрование и отправка
            encrypted = cipher.encrypt(data)
            client.sendall(encrypted)
            print(f"[{datetime.now()}] [↑] Отправлено {len(encrypted)} байт")
            
            # Получение ответа
            response = client.recv(65536)
            decrypted = cipher.decrypt(response).decode()
            
            # Обработка ping
            if choice == "3":
                rtt = (datetime.now() - start_time).total_seconds() * 1000
                print(f"[{datetime.now()}] [↓] Ответ сервера: {decrypted}")
                print(f"[{datetime.now()}] [*] Ping успешен! RTT: {rtt:.2f} мс")
            else:
                print(f"[{datetime.now()}] [↓] Ответ сервера: {decrypted}")
                
    except Exception as e:
        print(f"[{datetime.now()}] [!] Ошибка: {str(e)}")
    finally:
        client.close()
        print(f"[{datetime.now()}] [*] Соединение закрыто")

if __name__ == "__main__":
    main()