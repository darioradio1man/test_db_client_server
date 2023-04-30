import socket
from datetime import datetime
import db
# import ast

address = ('localhost', 26709)
max_size = 1000
print('Starting the server at', datetime.now())
print('Waiting for a client to call.')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(5)
client, addr = s.accept()

db = db.CustomDB(['name', 'birthday'])

mydata = client.recv(1024).decode()
print(mydata)
while True:
    try:
        mydata = client.recv(1024).decode()
        print('Query: {}'.format(mydata))
        value = None
        if mydata.lower() == "exit":
            break
        # elif mydata.lower().split()[0] == 'add':
        #     value = db.add_records()
        elif mydata.lower().split()[0] == 'delete':
            value = db.delete_records(int(mydata.lower().split()[1]))
        elif mydata.lower().split()[0] == 'changes':
            value = db.show_last_changes(int(mydata.lower().split()[1]))
        elif mydata.lower().split()[0] == 'show_db':
            value = db.sliding_window()
        print("The final result is:  " + str(value))
        client.sendall(str(value).encode())
    except EOFError:
        break

client.close()
s.close()
