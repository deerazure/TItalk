import threading
import socket

host = '127.0.0.1' # localhost
port = 7170

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} DISCONNECTED!'.encode('ascii'))
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('GIVENICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is {nickname}.')
        broadcast(f'{nickname} JOINED!'.encode('ascii'))
        client.send('CONNECTED TO CHATROOM'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        

print("Server is listening...")
receive()

