import socket
import sys
import threading
from datetime import datetime
from commands import *

address = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()
s.bind((address, port))
s.listen()

# Client class that keeps track of attributes of each connected client
class Client:
    def __init__(this, connection, source, name = None):
        this.connection = connection
        this.source = source
        #this.thread = thread
        this.name = name if name is not None else "Client"

# A method for client connections to be sent to a separate thread.
def clientConnection(client):
    while True:
        print("clientCOnnection")
        #Client sends a message
        msg = client.connection.recv(1024).decode()
        time = datetime.now().strftime("%H:%M")
        broadcastMsg = time +"   "+ client.name +": "+ msg
        print(broadcastMsg)

        # broadcast(broadcastMsg)

# Method that sends a message to all clients
#def broadcast():
    # Send message to all clients

#def command():
    # Client runs a command

# List of clients that have established a connection
clients = []

# Establishes a connection and creates a thread for each client
while True:
    connection, source = s.accept()
    client = Client(connection, source)
    #client = Client(connection, source, threading.Thread(target=clientConnection, args=(client,))
    print(client.source[0] +" connected!")

    clients.append(client)
    print(clients)
    t = threading.Thread(target=clientConnection, args=(client,))
    t.start()
