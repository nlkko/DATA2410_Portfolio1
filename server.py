import socket
import sys
from commands import *

address = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()
s.bind((address, port))
s.listen()

# List of clients that establish a connection
clients = []

# A method for client connections to be sent to a separate thread.
def clientConnection(connection, source):
    while True:



while True:
    connection, address = s.accept()
    clients.append(connection)
