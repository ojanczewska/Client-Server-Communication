import socket
from _thread import *
import os
import time
import msvcrt

class Client:

    def __init__(self):
        self.client_socket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 12345

        # connecting to the server
        print("Waiting for connection..")
        while True:
            try:
                self.client_socket.connect((self.host, self.port))
                response = self.client_socket.recv(1024)
                # message from the server what number is the client
                print('\n' + response.decode('utf-8'))
                break
            except socket.error as e:
                print(str(e))

        # launching threads
        start_new_thread(self.receive_message, ())
        start_new_thread(self.send_message, ())
        while True:
            pass

    # handling of sending messages (chat or doc document)
    def send_message(self):
            while True:
                receiver = input('\n'+'Enter the recipient: ')
                self.client_socket.send(str.encode(receiver))

                type = input('\n'+'Enter 0 if you want to send a text message, 1 if you want to send a document (* doc): ')
                self.client_socket.send(str.encode(type))

                time.sleep(0.1)
                type = int(type)

                # full duplex chat support, ending the chat after pressing enter
                if type == 0:
                    print(('Please enter your message: '))

                    massage_w = ""
                    while True:
                        pressed_key = msvcrt.getch()
                        massage_w = massage_w + pressed_key.decode('utf-8')
                        print(massage_w, end='\r')
                        self.client_socket.send(pressed_key)
                        if pressed_key == b"\r":
                            break

                # handling of sending the document doc
                elif type == 1:
                    filename = input('Enter a file name: ')
                    filesize = os.path.getsize(filename)
                    self.client_socket.send(str.encode(f'{filename}<SEPARATOR>{filesize}'))

                    f = open(filename, "rb")
                    while True:
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            print("End of sending")
                            time.sleep(0.2)
                            self.client_socket.send("koniec wysylania ".encode())
                            break

                        self.client_socket.send(bytes_read)
                    f.close()
                else:
                    print('There is no such operation')

    # handling of receiving messages
    def receive_message(self):
             while True:
                    # checking what type of message it is
                    type = self.client_socket.recv(1024).decode('utf-8')
                    type = int(type)

                    # reading from whom the message came
                    from_who= self.client_socket.recv(1024).decode('utf-8')
                    from_who = int(from_who)
                    print('\n' + f'Message from: {from_who}')

                    # handling incoming chat messages
                    if type == 0:
                        massage_w = ""
                        while True:
                            message = self.client_socket.recv(2048)
                            if message == b"\r":
                                print("\nend of message ")
                                break
                            message = message.decode('utf-8')
                            massage_w = massage_w + message
                            print(massage_w, end='\r')

                    # handling of the incoming doc
                    elif type == 1:
                        received = self.client_socket.recv(4096).decode()
                        filename, filesize = received.split("<SEPARATOR>")
                        filename = os.path.basename(f"{filename}_od_{from_who}.doc")

                        f = open(filename, "w")
                        while True:
                            bytes_read = self.client_socket.recv(1024)
                            if bytes_read.decode('utf-8') == "koniec wysylania ":
                                break
                            f.write(bytes_read.decode('utf-8'))
                        f.close()
                        print(f"Document received {filename}")

myClient = Client()

