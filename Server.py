import socket
import os
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

print('Waiting for a Connection..')
ServerSocket.listen(5)

ThreadID = 0
choices_list = ["rock", "paper", "scissors", "lizard", "spock"]


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
def threaded_client(connection):
    connection.send(str.encode('Welcome to the RPSLS Game!'))
    
    player_score = 0
    opponent_score = 0
    while True:
        data = connection.recv(2048)

        winner, opponent_choice = get_winner(data.decode('utf-8'))   # return True if human player won, False otherwise and opponent's choice
        reply = "Your opponent chose " + opponent_choice
        if winner == True: 
            player_score += 1
            reply += ". You won! "
        else:
            opponent_score +=1
            reply += ". You lost! "

        reply += "Current score: You - " + str(player_score) + " Opponent - " + str(opponent_score)

        connection.sendall(str.encode(reply))

        data = connection.recv(2048)
        if data.decode('utf-8') == "n":
            break

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
