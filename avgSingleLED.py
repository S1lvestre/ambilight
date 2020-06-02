import mss
import numpy as np

import serial
import time

def avg(img):
    return np.mean(img, axis=(0,1)) # (blue, green, red)

def colorWrite(r, g, b):
    print("R,G,B = " + str(r) + ","+ str(g) + "," + str(b))
    ser.write((str(r) + ","+ str(g) + "," + str(b) + "\n").encode())

ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)

with mss.mss() as sct:

    bgr = np.zeros((4,), dtype=int)
    
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 50, "height": 50}

    while True:
    	# Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        bgr = avg(img).astype(int)

        #print("bgr = ", bgr) # *floor not round
        #print("rgb = ", bgr[2], bgr[1], bgr[0], "\n") 
        colorWrite(bgr[2], bgr[1], bgr[0])
