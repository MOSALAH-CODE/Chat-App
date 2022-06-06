import socket
import threading

# Sunucu icin 3 fonksiyona ihtiyacimiz var.

# 1. fonksiyon: sadece bagli tum istemcilere bir mesaj
# gonderen bir islevdir.

# 2. fonksiyon: yeni istemcilerin baglanmasini dinleyerek
# yeni baglantilari kabul edecek olan islevdir

# 3. fonksiyon: istemciye olan bireysel baglantilari
# ele alacak bir tutamac islevi


# Connection Data
host = '127.0.0.1'
port = 7500

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (internet socket, tcp socket)
server.bind((host, port))  # Connecting The Server
server.listen()  # Start Listing To The Clients

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Tüm Bağlı İstemcilere Mesaj Gönderme
def broadcast(message):
    for client in clients:
        client.send(message)


# Müşterilerden Gelen Mesajları İşleme
def handle(client):
    while True:
        try:
            # Yayın Mesajları
            message = client.recv(1024) # 1024 byte
            print(message.decode('ascii'))
            broadcast(message)
        except ConnectionResetError:
            # İstemcileri Kaldırma ve Kapatma
            index = clients.index(client)
            clients.remove(client)
            client.close()
            print(f'{nicknames[index]} left the chat!')
            broadcast(f'{nicknames[index]} left the chat!'.encode('ascii'))
            nicknames.remove(nicknames[index])
            break


# Alma ve Dinleme İşlevi
def receive():
    while True:
        # Bağlantıyı Kabul Etme
        client, address = server.accept()
        print(f"Connected with {str(address)} ", end="")

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f"- Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
