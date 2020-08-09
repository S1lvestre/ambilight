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

numLEDS = 84
zonesCount = [26, 16]    # top/bottom, left/right
zonesDism = [72, 36, 24] # length, width, offset

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

ser = serial.Serial("/dev/ttyACM0", baudrate = 9600)
print("\nSerial port /dev/ttyACM0 opened;\nBaudrate 9600\n")

waitForMessage("Arduino is Ready")
arduinoIsReady = True

while True:
    if arduinoIsReady :
        # get frame of colors
        with mss.mss() as sct:
            goingOut = "<"

            # Get raw pixels from the screen, save it to a Numpy array
            img = np.array(sct.grab(monitor))[:,:,:3]
            
            # top row
            for top_i in range(zonesCount[0]) :
                zone = img[0:15, (72*top_i)+24 : (72*(top_i+1))+24]
                avrgColor = calcAvrg(zone)
                goingOut += rgbToStr(avrgColor)
            
            #top right
            zone = img[0:15, -15:1920]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
            
            # right row
            for right_i in range(zonesCount[1]-2):
                zone = img[(72*right_i)+15 : (72*(right_i+1))+15 , -15:1920 ]
                avrgColor = calcAvrg(zone)
                goingOut += rgbToStr(avrgColor)
            
            #bot right
            zone = img[-15:1080, -15:1920]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)

            # bottom row
            for bot_i in range(zonesCount[0]) :
                zone = img[-15:1080, (72*bot_i)+24 : (72*(bot_i+1))+24  ]
                avrgColor = calcAvrg(zone) 
                goingOut += rgbToStr(avrgColor)
            
            #bot left
            zone = img[-15:1080, 0:15]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)

            # left row
            for left_i in range(zonesCount[1]-2):
                zone = img[(72*left_i)+15 : (72*(left_i+1))+15 , 0:36 ]
                avrgColor = calcAvrg(zone)
                goingOut += rgbToStr(avrgColor)
            
            #top left
            zone = img[0:15, 0:15]
            avrgColor = calcAvrg(zone)
            goingOut += rgbToStr(avrgColor)
            
            goingOut += '>'
        
        # send next frame of colors
        ser.write(goingOut.encode())
        arduinoIsReady = False
        
        print( "╔═══════ PC ══════════════"   )
        print( "║     Sent: " + goingOut      )
        print( "╚═════════════════════════\n" )

    else :
        # wait for signal from arduino
        waitForMessage("Send Next")
        arduinoIsReady = True

ser.close
print("Serial port /dev/ttyACM0 closed;\n")


