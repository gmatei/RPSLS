import socket
import os
from threading import *
import threading
from time import sleep

# Socket and connection setup
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

ThreadID = 0

#Thread use for communication with each client
def threaded_client(connection):
    connection.send(str.encode('Welcome to the RPSLS Game!'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

#Used for accepting client connections
while True:
    if(threading.active_count() <= 3):
        Client, address = ServerSocket.accept()     #Accept new client
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        
        thread = Thread(target = threaded_client, args = (Client, )) #Start new thread for client
        thread.start()

        #start_new_thread(threaded_client, (Client, ))   #Start new thread for client
        ThreadID += 1
        print('Thread Number: ' + str(ThreadID))

#Close the server when?
ServerSocket.close()
