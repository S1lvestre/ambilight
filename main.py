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

monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

startMarker = ord('<')
endMarker = ord('>')





#=========================
#
# FUNCTION DEFINITIONS
#
#=========================

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

##########################################
#colors = "<0x000000;0x000000;0x000000;>"#
##########################################

while True:
    if arduinoIsReady :
        # get frame of colors
        with mss.mss() as sct:
            img = np.array(sct.grab(monitor))[:,:,:3]
#         ->
#         ->
#         ->
#         ->
#         ->
#         ->
#         ->

            #color = qq coisa

        # send next frame of colors
#     ->ser.write(colors.encode())
        arduinoIsReady = False
        
        #print( "Test " + str(n) + '\n'        )
        #print( "╔═══════ PC ══════════════"   )
        #print( "║     Sent: " + colors        )
        #print( "╚═════════════════════════\n" )

    else
        # wait for signal from arduino
        waitForMessage("Send Next")
        arduinoIsReady = True









ser.close
print("Serial port /dev/ttyACM0 closed;\n")


