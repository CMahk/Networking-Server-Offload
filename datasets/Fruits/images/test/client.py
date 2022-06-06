import socket
import os
import time

import logging
logging.basicConfig(level=logging.INFO, filename="client.log", filemode="w", format="%(levelname)s - %(message)s")

path = os.path.abspath(os.path.dirname(__file__))
port = 25565
host = "128.110.219.91"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

logging.info("Socket successfully created") 
       
f = open(path + "/2.jpg", 'rb')
l = f.read(1024)

start = time.time()
while (l):
    client.send(l)
    print('Sent ', repr(l))
    l = f.read(1024)
f.close()
end = time.time()

logging.info('Successfully sent the file')
logging.info('Time to send image file: ' + str(end - start) + ' sec')
logging.info('Connection closed')
