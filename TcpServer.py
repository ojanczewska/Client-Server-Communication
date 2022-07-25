import socket
from _thread import *
import time


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 12345
        self.ThreadCount = 0
        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))

        print("Serwer waiting for connection..")
        self.server_socket.listen(5)
        self.clients = []

        while True:
            client, address = self.server_socket.accept()

            print(f"Conneted to Klient {self.ThreadCount} {address[0] } {str(address[1])}")

            client.send(str.encode(f"Welcome to the server, you are the client nr {self.ThreadCount}"))

            start_new_thread(self.client_thread, (client,self.ThreadCount))
            self.ThreadCount += 1
            self.clients.append(client)
            print("Thread number = " + str(self.ThreadCount))

    def client_thread(self, connection,number):

        while True:

            receiver = connection.recv(1024).decode('utf-8')
            receiver = int(receiver)

            type = connection.recv(2048).decode('utf-8')
            type = int(type)

            if type == 0:

                self.clients[receiver].sendall(str.encode(str(0)))
                time.sleep(0.1)

                self.clients[receiver].sendall(str.encode(str(number)))
                time.sleep(0.1)

                massage_w = ""
                while True:
                    message = connection.recv(2048)
                    self.clients[receiver].sendall(message)

                    if message == b"\r":
                        break

                    message = message.decode('utf-8')
                    massage_w = massage_w + message

                print(f'\nFrom: client nr {number}')
                print(f'To : client nr {receiver}')
                print('Message:' + massage_w)

            elif type == 1:
                self.clients[receiver].sendall(str.encode(str(1)))
                time.sleep(0.1)

                self.clients[receiver].sendall(str.encode(str(number)))
                time.sleep(0.1)

                received = connection.recv(4096)
                self.clients[receiver].sendall(received)
                time.sleep(0.1)

                filename, filesize = received.decode('utf-8').split("<SEPARATOR>")

                time.sleep(0.1)

                while True:
                    bytes_read = connection.recv(1024)
                    if bytes_read.decode('utf-8') == "koniec wysylania ":
                        self.clients[receiver].send(bytes_read)
                        break
                    self.clients[receiver].send(bytes_read)

                print(f'From:  client nr {number}')
                print(f'To : client nr {receiver}')
                print(f'Document sent {filename}')

        connection.close()

myServer = Server()