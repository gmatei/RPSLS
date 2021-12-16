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
Response = ClientSocket.recv(1024)  # Read welcome message
print(Response.decode('utf-8'))

playAgain = True
while playAgain:
    
    Input = "none"
    while Input == "none":
        Input = input('Choose rock / paper / scissors / lizard / spock: ')
        if Input not in ["rock", "paper", "scissors", "lizard", "spock"]:
            print("Invalid choice. Try again!")
            Input = "none"
    
    ClientSocket.send(str.encode(Input))    # Send player choice to server
    
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))     # Get response
    
    Input = "none"
    while Input == "none":
        Input = input('Would you like to play again? (y/n) ')   # Initiate another game session if wanted
        if Input not in ["y", "n"]:
            print("Invalid response. Try again!")
            Input = "none"
    
    ClientSocket.send(str.encode(Input))
    if Input == "n":
        playAgain = False
        print("Thank you for playing!")

ClientSocket.close()
