import os
from os import walk
import PIL
from PIL import Image
import time
import torch
import sys
import io

import logging
logging.basicConfig(level=logging.INFO, filename="model.log", filemode="w", format="%(levelname)s - %(message)s")

logging.info("Loading model")

# Load images and create different resolutions
path = os.path.abspath(os.path.dirname(__file__))
ptt = path + "/datasets/Fruits/images/test/lower_res/"
f = []

if not (os.path.isdir(ptt)):
    os.mkdir(ptt)

for (_, _, filenames) in walk(path + "/datasets/Fruits/images/test/"):
    f.extend(filenames)
    break

# Load model
ptweight = path + "/yolov5/fruit_weights/600"
time_start = time.time()
model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)
time_end = time.time()

time_load = "{0:.4f}".format(time_end - time_start) + " sec"
logging.info("Model loading time: " + time_load)
logging.info("Model successfully loaded")

for image in filenames:
    im = path + "/datasets/Fruits/images/test/" + image
    split_im = image.split(".")
    img = PIL.Image.open(im)
    width, height = img.size
    
    new_image1 = img.resize((int(width * 0.8), int(height * 0.8)))
    new_image1.save(ptt + split_im[0] + "_08.jpg")

    new_image2 = img.resize((int(width * 0.6), int(height * 0.6)))
    new_image2.save(ptt + split_im[0] + "_06.jpg")

    new_image3 = img.resize((int(width * 0.4), int(height * 0.4)))
    new_image3.save(ptt + split_im[0] + "_04.jpg")

    new_image4 = img.resize((int(width * 0.2), int(height * 0.2)))
    new_image4.save(ptt + split_im[0] + "_02.jpg")
        
    images = [im, ptt + split_im[0] + "_08.jpg", ptt + split_im[0] + "_06.jpg", ptt + split_im[0] + "_04.jpg", ptt + split_im[0] + "_02.jpg"]

    # Model Inference
    run_start = time.time()
    results = model(images)  # includes NMS
    run_end = time.time()

    model_run = run_end - run_start
    run_time = "Model running time: " + "{0:.4f}".format(model_run) + " sec"
    logging.info(run_time)

    # Model Results
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    results.print()
    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    logging.info(output)
    results.save()  # or .show()

    results.xyxy[0]  # im1 predictions (tensor)
    results.pandas().xyxy[0]
