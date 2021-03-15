import socket
import sys
import threading
from datetime import datetime
import inspect

address = "localhost"
port = int(sys.argv[1])

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
    # Maintaining clients list by checking if client is still connected, if not removing client
    try:
        # Client sends a message
        while True:
            msg = client.connection.recv(1024)
            if msg: # Check if a message has been sent
                msg = msg.decode()

                time = datetime.now().strftime("%H:%M")
                broadcastMsg = time +"   "+ client.name +": "+ msg
                print(broadcastMsg)
                broadcast("\n"+broadcastMsg, client)
    except:
        print("Connection closed with: "+ client.source[0]+", "+client.name)
        client.connection.close()
        clients.remove(client)

# Method that sends a message to all clients
def broadcast(broadcastMsg, client):
    # Send message to all clients
    for c in clients:
        if c is not client:
            c.connection.send(broadcastMsg.encode())

# Establishes a connection and creates a thread for each client
while True:
    connection, source = s.accept()
    name = connection.recv(1024).decode()
    client = Client(connection, source, name = name)
    print(client.source[0]+", "+ client.name +" connected!")
    clients.append(client)

    # Starting thread
    t = threading.Thread(target=clientConnection, args=(client,))
    client.thread = t
    client.thread.start()