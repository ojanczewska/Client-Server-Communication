import subprocess
import time

"Script to launch separate consoles for the server and clients"

# number of clients to be created
clients = int(input("Enter the number of clients: "))
# opening the console for servicing the server
subprocess.call(f'start python TcpServer.py',  shell = True)

# opening the console for servicing clients
time.sleep(1)
for i in range(clients):
    subprocess.call(f'start python TcpClient.py',  shell = True)