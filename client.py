import socket
import os
from os import walk
import PIL
from PIL import Image
import time
import pickle

# Establish connection
path = os.path.abspath(os.path.dirname(__file__))
port = 25565
host = "128.110.219.124"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Load images and create different resolutions
ptt = path + "/datasets/Fruits/images/test/lower_res/"
f = []

if not (os.path.isdir(ptt)):
    os.mkdir(ptt)

for (_, _, filenames) in walk(path + "/datasets/Fruits/images/test/"):
    f.extend(filenames)
    break

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
    
    for fruit in images:
        f = open(fruit, 'rb')
        l = f.read(1028)
        while (l):
            client.send(l)
            print("Sent portion of " + fruit)
            l = f.read(1028)
        f.close()
        client.send("EOF".encode())

        reply = client.recv(256)
        if (reply == b"\xFF\xFF"):
            print("CONTINUING")
            continue
        else:
            print(reply)
            print("WHAAAAT")

client.send("EOD".encode())

with open("performance.log", "wb") as f:
    metrics = client.recv(1028)
    while (metrics):
        f.write(metrics)
        metrics = client.recv(1028)
f.close()

client.close()
print("Completed.")
