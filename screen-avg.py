import serial
import time

ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)

def colorWrite(r, g, b):
    print("R,G,B = " + str(r) + ","+ str(g) + "," + str(b))
    ser.write((str(r) + ","+ str(g) + "," + str(b) + "\n").encode())

def test_colorWrite():
    i = 0
    while i < 10:
        colorWrite(255, 0, 0)
        time.sleep(.1)

        colorWrite(0, 255, 0)
        time.sleep(.1)
        
        colorWrite(0, 0, 255)
        time.sleep(.1)
        
        i += 1

    colorWrite(0, 0, 0)

#test_colorWrite()

#while True == False:
    #colorWrite(0, 0, 0)
