import socket
import cv2
import torch
import os
from PIL import Image

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
    
    # Model
    pt = os.path.abspath(os.path.dirname(__file__))
    ptweight = pt + "/yolov5/fruit_weights/600"
    print("PATH: " + pt)
    model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)

    im = pt + "/received_file.jpg"

    # Inference
    results = model(im)  # includes NMS

    # Results
    results.print()  
    results.save()  # or .show()

    results.xyxy[0]  # im1 predictions (tensor)
    results.pandas().xyxy[0]
