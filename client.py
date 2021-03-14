import socket
import sys
import threading

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
        msg = c.recv(1024)
        if msg: # Check if a message has been sent
            msg = msg.decode()
            print(msg)

# Client either recieves or sends a message to the server
# Creating a thread for each action enables them work simultaneously 

# Client sends a message
sendThread = threading.Thread(target=sendMessage)
sendThread.start()

# Client recieves a message
recvThread = threading.Thread(target=recieveMessage)
recvThread.start()

