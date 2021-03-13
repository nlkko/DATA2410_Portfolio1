import socket
import sys
import threading
from datetime import datetime

address = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]

c = socket.socket()
c.connect((address, port))

def sendMessage():
    while True:
        msg = input("Send: ")
        c.send(msg.encode())

def recieveMessage():
    while True:
        msg = c.recv(1024).decode()
        print(msg)

#OBS Må lage en egen thread for å sende og motta melding
#while True:
    #Client either recieves or sends a message to the server

# Client sends a message
sendThread = threading.Thread(target=sendMessage)
sendThread.start()

# Client recieves a message
recvThread = threading.Thread(target=recieveMessage)
recvThread.start()

