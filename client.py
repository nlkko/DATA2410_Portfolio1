import socket
import sys

address = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]

c = socket.socket()
c.connect((address, port))