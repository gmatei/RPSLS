import socket
from threading import *
import threading
from time import sleep
import random

# Socket and connection setup
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection...')
ServerSocket.listen(5)
ServerSocket.settimeout(0.5)


ThreadID = 0
choices_list = ["rock", "paper", "scissors", "lizard", "spock"]

# Generate opponent choice and return winner (True - player / False - opponent)
def get_winner(player_choice):
    opponent_choice = choices_list[random.randint(0,4)]

    if player_choice == "rock" and (opponent_choice == "scissors" or opponent_choice == "lizard"):
        return True, opponent_choice
    elif player_choice == "paper" and (opponent_choice == "rock" or opponent_choice == "spock"):
        return True, opponent_choice
    elif player_choice == "scissors" and (opponent_choice == "paper" or opponent_choice == "lizard"):
        return True, opponent_choice
    elif player_choice == "lizard" and (opponent_choice == "spock" or opponent_choice == "paper"):
        return True, opponent_choice
    elif player_choice == "spock" and (opponent_choice == "scissors" or opponent_choice == "rock"):
        return True, opponent_choice
    else:
        return False, opponent_choice

#Thread use for communication with each client
def threaded_client(connection, address):
    connection.send(str.encode('Welcome to the RPSLS Game!'))
    
    player_score = 0
    opponent_score = 0
    while True:
        data = connection.recv(2048)

        winner, opponent_choice = get_winner(data.decode('utf-8'))
        reply = "Your opponent chose " + opponent_choice
        server_log = "Server played against " + str(address) + ". Server chose " + opponent_choice + ". Player chose " + data.decode('utf-8')

        if winner == True: 
            player_score += 1
            reply += ". You won! "
            server_log += ". Player won! "
        else:
            opponent_score +=1
            reply += ". You lost! "
            server_log += ". Server won! "

        reply += "Current score: You - " + str(player_score) + " Opponent - " + str(opponent_score)
        server_log += "Current score: Player - " + str(player_score) + " Server - " + str(opponent_score)

        connection.sendall(str.encode(reply))

        print(server_log)

        data = connection.recv(2048)
        if data.decode('utf-8') == "n":
            break

    connection.close()

#Used for accepting client connections
try:
    while True:
        if(threading.active_count() <= 3):
            try:
                Client, address = ServerSocket.accept()     #Accept new client
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                
                thread = Thread(target = threaded_client, args = (Client, address)) #Start new thread for client
                thread.daemon = True
                thread.start()

                ThreadID += 1
                print('Thread Number: ' + str(ThreadID))
            except socket.timeout:
                pass
except KeyboardInterrupt:
    print("Server closed!")

#Close the server
ServerSocket.close()
