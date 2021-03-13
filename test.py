while True:
    connection, source = s.accept()
    client = Client(connection, source)
    #client = Client(connection, source, threading.Thread(target=clientConnection, args=(client,))
    print(client.source[0] +" connected!")

    clients.append(client)
    print(clients)
    t = threading.Thread(target=clientConnection, args=(client,))
    t.start()

def clientConnection(client):
    while True:
        print("clientCOnnection")
        #Client sends a message
        msg = client.connection.recv(1024).decode()
        time = datetime.now().strftime("%H:%M")
        broadcastMsg = time +"   "+ client.name +": "+ msg
        print(broadcastMsg)

        # broadcast(broadcastMsg)

def recieveMessage():
    while True:
        print("hei")
        msg = c.recv(1024).decode()
        if msg != "":
            print(msg)