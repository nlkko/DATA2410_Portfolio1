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

# List of clients that have established a connection
clients = []

# Client class that keeps track of attributes of each connected client
class Client:
    def __init__(this, connection, source, thread = None, name = None):
        this.connection = connection
        this.source = source
        this.thread = thread
        this.name = name if name is not None else "Client"

# A method for client connections to be sent to a separate thread.
def clientConnection(client):
    # Client sends a message
    while True:
        msg = client.connection.recv(1024).decode()
        if msg != "":
            time = datetime.now().strftime("%H:%M")
            broadcastMsg = time +"   "+ client.name +": "+ msg
            print(broadcastMsg)
            broadcast(broadcastMsg)

# Method that sends a message to all clients
def broadcast(broadcastMsg):
    # Send message to all clients
    for client in clients:
        print("Client: "+ client.source[0])
        client.connection.send(broadcastMsg.encode())
        

#def command():
    # Client runs a command

# Establishes a connection and creates a thread for each client
while True:
    connection, source = s.accept()
    client = Client(connection, source)
    print(client.source[0] +" connected!")

    # Starting the thread
    t = threading.Thread(target=clientConnection, args=(client,))
    client.thread = t
    client.thread.start()

    
