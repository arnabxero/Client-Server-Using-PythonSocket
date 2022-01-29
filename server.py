import socket
import threading

clients = []
number_clients = 0


class Client(threading.Thread):
    
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
                
                if data != "":
                    print("Client ID " + str(self.id) + " Sent Data = '" + str(data.decode("utf-8"))+"'")
                
                
                for client in clients:
                    if client.id == self.id:
                        print(" |------ Replying to Client : " + str(data.decode("utf-8")))
                        client.socket.sendall(data)
                    
                    
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                clients.remove(self)
                break
                    
                    
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global number_clients
        clients.append(Client(sock, address, number_clients, "Name", True))
        clients[len(clients) - 1].start()
        print("New client connected, Assigned ID is = " + str(clients[len(clients) - 1]))
        number_clients += 1
        
        
def main():
    print("If you are using on local machine enter\nhost = localhost\nPort = 0-65535(any)")
    host = input("Host: ")
    port = int(input("Port: "))

    print("Server Started");
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()