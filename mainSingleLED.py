import mss
import numpy as np

import serial
import time

import color

def colorWrite(r, g, b):
    #print("R,G,B = " + str(r) + ","+ str(g) + "," + str(b))
    ser.write((str(r) + ","+ str(g) + "," + str(b) + "\n").encode())
    
ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)

with mss.mss() as sct:

    bgr = np.zeros((4,), dtype=int)
    
    # Part of the screen to capture
    monitor = {"top": 500, "left": 500, "width": 100, "height": 100}
    
    while True:
         
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))[:,:,:3]
        data = np.reshape( img, (np.shape(img)[0]*np.shape(img)[1], 3) )
        
        # Get dominant color
        clusts, dominants = color.kmeans(5, 5, data)
        dom = color.getDominant(clusts, dominants)
        
        # Send to arduino IN bgr format
        colorWrite(dom[2], dom[1], dom[0])
