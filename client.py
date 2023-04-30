import socket
from datetime import datetime

address = ('localhost', 26709)
max_size = 1000
print('Starting the client at', datetime.now())
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)
client.sendall(b'Hey!')

while True:
    mydata = input("> ")
    client.send(mydata.encode())
    if mydata.lower() == 'exit':
        break
    data = client.recv(1024).decode()
    print('At', datetime.now(), 'someone replied', data)
client.close()
