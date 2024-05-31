import socket

# Создание сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение к серверу
client_socket.connect(('192.168.0.119', 12345))

# Отправка данных серверу
client_socket.send('Привет, сервер!'.encode('utf-8'))

# Получение данных от сервера
data = client_socket.recv(1024)
print('Получено:', data.decode('utf-8'))

# Закрытие соединения
client_socket.close()
