#Noam Sabban 329897391
#Hadas Dahan 205636970

import socket
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432

def main():
    # checking if the player wants to play
    openingMsp = input("Do you want to play? Y=yes, N=no\n")
    if (openingMsp == 'Y'):
        # connecting to server
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))

        #dealing with reciving and sending to server
        message = conn.recv(512) # read block response is 512 bytes long

        if len(message) > 0:
            while not ("Player choose not to play" in message.decode()):
                # printing the message from the server

                print(message.decode())
                response = input("")

                # send the response to the server
                conn.send(bytes(response, "utf-8"))
                message = conn.recv(512)

            #player chose not to play again - end of game
            print(message.decode())
            conn.close()

    elif (openingMsp == 'N'):
        # ending the program
        sys.exit("Player choose not to play")

if __name__ == "__main__":
    main()