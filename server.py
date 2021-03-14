import socket
import sys
import threading
from datetime import datetime
from commands import *
import inspect

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
        msg = client.connection.recv(1024)
        if msg: # Check if a message has been sent
            msg = msg.decode()
            if msg[0] == "/":
                command(client, msg)
            else:
                time = datetime.now().strftime("%H:%M")
                broadcastMsg = time +"   "+ client.name +": "+ msg
                print(broadcastMsg)
                broadcast(broadcastMsg)

# Method that sends a message to all clients
def broadcast(broadcastMsg):
    # Send message to all clients
    for client in clients:
        client.connection.send(broadcastMsg.encode())        

# Method that enables clients to run specific commands
def command(client, msg):
    # Client runs a command
    exist = False
    for command in commands:
        if msg.split()[0] == command:
            argins = len(inspect.getfullargspec(command).args)
            globals()[command[1:]](lambda argins: None if argins == 0 else msg.split()[1])
            exist = True
    
    # Error sent to client if command does not exist
    if not exist:
        client.connection.send("Command does not exist, type /help for a list of all commands.".encode())


# Establishes a connection and creates a thread for each client
while True:
    connection, source = s.accept()
    client = Client(connection, source)
    print(client.source[0] +" connected!")
    clients.append(client)

    # Starting the thread
    t = threading.Thread(target=clientConnection, args=(client,))
    client.thread = t
    client.thread.start()