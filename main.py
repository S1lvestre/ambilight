#=========================
#
# LIBRARIES
#
#=========================

import mss
import numpy as np

import serial
import time



#=========================
#
# VARIABLES
#
#=========================

numLEDS = 78
zonesCount = [26, 16]    # top/bottom, left/right

zonesL = 72
zonesW = 10
zonesOffst = 24

# Part of the screen to capture
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}



startMarker = ord('<')
endMarker = ord('>')



#=========================
#
# FUNCTION DEFINITIONS
#
#=========================

def calcAvrg(array) :
    """ receives (i,j,3) array, 
        turns into i*j by 3,
        calcs avrg for each channel """
    
    elmCount = np.shape(array)[0]*np.shape(array)[1]

    data = np.reshape( array, (elmCount, 3) )
    
    color = np.round(np.sum( data, axis = 0 ) / elmCount).astype(np.uint8)

    return color


def rgbToStr(rgb) :
    """  """

    string = '0x%02x%02x%02x;' % (rgb[0], rgb[1], rgb[2])

    return string



def waitForMessage(message):
    """ wait untill the arduino sends "message"
    (Allows time for arduino reset when used at boot)
    Ensures any bytes left from previous messages are discarded"""

    msg = ""
    while ( message in msg) == False:
        while ser.inWaiting() == 0:
            pass

        msg = recvFromArduino()
        print(msg + '\n')


def recvFromArduino():
    ck = ""
    x = 'z'
    byteCount = -1 # last char is endMarker

    while ord(x) != startMarker:
        x = ser.read()

    while ord(x) !=endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode()
            byteCount += 1
        x = ser.read()

    return(ck)

#=========================
#
# MAIN
#
#=========================

ser = serial.Serial("/dev/ttyACM0", baudrate = 500000) # 187800
print("\nSerial port /dev/ttyACM0 opened;\nBaudrate 187800\n")

waitForMessage("Arduino is Ready")
arduinoIsReady = True

while True:
    t0 = time.time()

    # get frame of colors
    with mss.mss() as sct:
        goingOut = "<"
        
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))[:,:,:3]
         
        #bot left
        for i in range(9):
            zone = img[-25:1080 , 584-(73*i):658-(73*i)]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
         
        #left
        for i in range(16):
            zone = img[ 1013-(67*i):1080-(67*i) , 0:25]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
        
        # top row
        for top_i in range(28) :
            zone = img[0:25, (68*top_i): (68*(top_i+1))]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
        
        #right
        for i in range(16):
            zone = img[ 0+(67*i):67+(67*i) , -25:1920]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
        
        #bot right
        for i in range(9):
            zone = img[-25:1080 , 1847-(73*i):1921-(73*i)]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
        
        goingOut += '>'
    t1 = time.time()

    # send next frame of colors
    ser.write(goingOut.encode())
    #arduinoIsReady = False
    
    t2 = time.time()



    print( "╔══════ PC ═══════════════"   )
    print( "║     Sent: " + goingOut      )
    print( "╚═════════════════════════\n" )

    print( "╔═════ TIME (s) ══════════"   )
    print( "║      Loop : ", t1-t0        )
    print( "║ ser.write : ", t2-t1        )
    print( "║     Total : ", t2-t0        )
    print( "╚═════════════════════════\n" )

    
    
ser.close
print("Serial port /dev/ttyACM0 closed;\n")


