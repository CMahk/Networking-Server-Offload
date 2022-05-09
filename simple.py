import cv2
import torch
import os
from PIL import Image

# Model
pt = os.path.abspath(os.path.dirname(__file__))
ptweight = pt + "/yolov5/fruit_weights/300"
print("PATH: " + pt)
model = torch.hub.load("ultralytics/yolov5", "custom", path = ptweight, force_reload = False)

im = pt + "/datasets/Fruits/images/test/1.jpg"

# Inference
results = model(im)  # includes NMS

# Results
results.print()  
results.save()  # or .show()

results.xyxy[0]  # im1 predictions (tensor)
results.pandas().xyxy[0]