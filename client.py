import socket
import threading

nickname = input("NAME: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7170))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'GIVENICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print("ERROR!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()  # Add parentheses to start the thread

# Start the write thread
write_thread = threading.Thread(target=write)
write_thread.start()  # Add parentheses to start the thread
