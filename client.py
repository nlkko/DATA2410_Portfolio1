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
    msg = input("Send: ")
    c.send(msg.encode())

#OBS Må lage en egen thread for å sende og motta melding
#while True:
    #Client either recieves or sends a message to the server
msg = input("SKriv melding:  ")
c.send(msg.encode())