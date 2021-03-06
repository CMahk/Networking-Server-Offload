import socket
import torch
import os
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import psutil
import time
import pickle
import math
import sys
import io

import logging
logging.basicConfig(level=logging.INFO, filename="server.log", filemode="w", format="%(levelname)s - %(message)s")

path = os.path.abspath(os.path.dirname(__file__))
ptt = path + "/images/"
modelLoaded = False
finished = False

port = 25565

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.connect(("8.8.8.8", 80))
host = server.getsockname()[0]
server.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen(5)

if not (os.path.isdir(ptt)):
    os.mkdir(ptt)

print("Server running on " + str(host) + " and port " + str(port))
conn, addr = server.accept()

count = 1
subcount = 0
run = True
while run:
    print('Got connection from', addr)

    image_results = []
    get_images = True

    while get_images:
        with open(path + "/images/" + str(count) + "_" + str(subcount) + ".jpg", "wb") as f:
            print("Opening file " + str(count) + "_" + str(subcount) + ".jpg")
            start_bw = psutil.net_io_counters().bytes_recv
            print("Receiving data for image...")

            time_image_start = time.time()
            while True:
                data = conn.recv(1028)
                print(data)

                if not data or (data.find(b"\x45\x4F\x44") >= 0):
                    run = False
                    get_images = False
                    finished = True
                    break

                if data.find(b"\x45\x4F\x46") >= 0:
                    end_bw = psutil.net_io_counters().bytes_recv
                    time_image_end = time.time()
                    bw_load = (end_bw - start_bw) / 1024
                    bw_usage = "Bandwidth usage for Image " + str(count) + "_" + str(subcount) + ".jpg: " + "{0:.4f}".format(bw_load) + " KB"
                    time_image_total = math.ceil((time_image_end - time_image_start) * 1000)
                    time_image_log = "Time taken for Image " + str(count) + "_" + str(subcount) + ".jpg: " + str(time_image_total) + " ms"
                    logging.info(bw_usage)
                    logging.info(time_image_log)
                    image_results.append(bw_usage)
                    break
                
                f.write(data)
        f.close()

        print("Image " + str(count) + "_" + str(subcount) + ".jpg DONE")
        subcount += 1


        if (subcount >= 5):
            get_images = False
        
        if (get_images):
            print("Continuing...")
            conn.send(b"\xFF\xFF")

    print('Done receiving')

    if not modelLoaded:
        logging.info("Loading model")
        # Model
        pt = os.path.abspath(os.path.dirname(__file__))
        ptweight = pt + "/yolov5/fruit_weights/600"
        load_start = time.time()
        model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)
        load_end = time.time()

        model_load = math.ceil((load_end - load_start) * 1000)
        logging.info("Model successfully loaded")
        load_time = "Model loading time: " + str(model_load) + " ms"
        logging.info(load_time)
        image_results.append(load_time)

        modelLoaded = True

    if not finished:
        im = path + "/images/" + str(count)
        images = [im + "_0.jpg", im + "_1.jpg", im + "_2.jpg", im + "_3.jpg", im + "_4.jpg"]

        # Inference
        run_start = time.time()
        results = model(images)  # includes NMS
        run_end = time.time()

        model_run = math.ceil((run_end - run_start) * 1000)
        run_time = "Model running time: " + str(model_run) + " ms"
        logging.info(run_time)
        image_results.append(run_time)

        # Results
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        results.print()  
        output = new_stdout.getvalue()
        sys.std_out = old_stdout

        logging.info(output)
        results.save()  # or .show()

        results.xyxy[0]  # im1 predictions (tensor)
        results.pandas().xyxy[0]

        count += 1
        subcount = 0

    if (run):
        conn.send(b"\xFF\xFF")
        print("Loading next imageset...")
    else:
        with open("server.log", "rb") as f:
            l = f.read(1028)
            while (l):
                conn.send(l)
                l = f.read(1028)
        f.close()
        print("Completed.")
