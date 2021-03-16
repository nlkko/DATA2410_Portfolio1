import socket
import sys
import threading
from bots import *
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
            
            #If the client wants to end the session they type "/quit"
            if msg == "/quit":
                print("Closing connection with server...")
                c.close()
                break

            c.send(msg.encode())
            print(time +"   "+ name +" ~ "+msg)
    except:
        print("Could not send message to server")

# Client recieves a message
def recieveMessage():
    try:
        while True:
            msg = c.recv(1024)
            if msg: # Check if a message has been sent
                msg = msg.decode()
                print("\n"+msg)
    except:
        print("Stopped recieving messages from server")
        c.close()

# Send the name of the client over to the server
c.send(name.encode())
print("======== BadBots Chat client ========")
# Client either recieves from or sends a message to the server
# Creating a thread for each action enables them work simultaneously 

# Client is either a real person or a bot
# Checking to see if it is a bot
isBot = False
for bot in bots:
    if bot == name:
        isBot = True

# Bot:
if isBot:
    botThread = threading.Thread(target=botMessage, args= (c, name))
    botThread.start()
# Real person:
else:
    sendThread = threading.Thread(target=sendMessage)
    sendThread.start()

    recvThread = threading.Thread(target=recieveMessage)
    recvThread.start()

