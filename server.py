import socket
import cv2
import torch
import os
from PIL import Image
import psutil
import time

import logging
logging.basicConfig(level=logging.INFO, filename="server.log", filemode="w", format="%(levelname)s - %(message)s")

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
        start_bw = psutil.net_io_counters().bytes_recv
        while True:
            print('Receiving data...')
            data = conn.recv(1024)
            if not data:
                end_bw = psutil.net_io_counters().bytes_recv
                bw_load = (end_bw - start_bw) / 1024 / 1024
                logging.info("Bandwidth used to send image: " + str(bw_load) + " MB")
                break
            f.write(data)
    f.close()

    print('Done receiving')
    conn.close()
    
    logging.info("Loading model")

    # Model
    pt = os.path.abspath(os.path.dirname(__file__))
    ptweight = pt + "/yolov5/fruit_weights/600"
    print("PATH: " + pt)
    load_start = time.time()
    model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)
    load_end = time.time()

    logging.info("Model successfully loaded")
    logging.info("Model loading time: " + str(load_end - load_start) + " sec")

    im = pt + "/received_file.jpg"

    # Inference
    run_start = time.time()
    results = model(im)  # includes NMS
    run_end = time.time()

    logging.info("Model running time: " + str(run_end - run_start) + " sec")

    # Results
    results.print()  
    results.save()  # or .show()

    results.xyxy[0]  # im1 predictions (tensor)
    results.pandas().xyxy[0]
