import socket

# Socket and connection setup
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')

# Connect to the server
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

# Communication with the server
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()