import socket
import sys
import threading
from datetime import datetime

address = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]

c = socket.socket()
c.connect((address, port))

# Client sends a message
def sendMessage():
    try:
        while True:
            time = datetime.now().strftime("%H:%M")
            msg = input("Write a message: ")
            
            if msg == "/quit":
                print("Closing connection with server...")
                c.close()
                break

            c.send(msg.encode())
            print(time +"   "+ name +": "+msg)
    except:
        print("Could not send message to server")

# Client recieves a message
def recieveMessage():
    try:
        while True:
            msg = c.recv(1024)
            if msg: # Check if a message has been sent
                msg = msg.decode()
                print(msg)
    except:
        print("Stopped recieving messages from server")
        c.close()

# Send the name of the client over to the server
c.send(name.encode())

# Client either recieves from or sends a message to the server
# Creating a thread for each action enables them work simultaneously 
sendThread = threading.Thread(target=sendMessage)
sendThread.start()

recvThread = threading.Thread(target=recieveMessage)
recvThread.start()