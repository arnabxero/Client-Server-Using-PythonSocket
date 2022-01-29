import socket
import threading
import sys


def receive(socket, signal):
    print("Started Receiving Server Replies")

    while signal:
        try:
            data = socket.recv(32)
            print("Server Replied Data = ' Got From Client = " + str(data.decode("utf-8")) + "'")
        except:
            print("You have been disconnected from the server")
            signal = False
            break

host = input("Host: ")
port = int(input("Port: "))

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Successfully Connected to Server")
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

while True:
    message = input()
    sock.sendall(str.encode(message))