import cv2
import torch
import os
from PIL import Image
import time

import logging
logging.basicConfig(level=logging.INFO, filename="model.log", filemode="w", format="%(levelname)s - %(message)s")

logging.info("Loading model")

# Model
pt = os.path.abspath(os.path.dirname(__file__))
ptweight = pt + "/yolov5/fruit_weights/300"
print("PATH: " + pt)
start = time.time()
model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)

logging.info("Model successfully loaded")

im = pt + "/datasets/Fruits/images/test/1.jpg"

# Inference
results = model(im)  # includes NMS
end = time.time()

logging.info("Model running time: " + str(end - start) + " sec")

# Results
results.print()  
results.save()  # or .show()

results.xyxy[0]  # im1 predictions (tensor)
results.pandas().xyxy[0]
