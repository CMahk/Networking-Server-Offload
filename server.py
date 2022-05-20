import socket
import os

path = os.path.abspath(os.path.dirname(__file__))
port = 25565

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.connect(("8.8.8.8", 80))
host = server.getsockname()[0]
server.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

print("Server running on " + str(host) + " and port " + str(port))

while True:
    conn, addr = server.accept()
    print('Got connection from', addr)
    
    with open(path + "/received_file.jpg", "wb") as f:
        print('Opening file...')
        while True:
            print('Receiving data...')
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
    f.close()
    
    print('Done receiving')
    conn.close()
