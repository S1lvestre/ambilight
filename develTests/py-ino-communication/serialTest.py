import serial
import time

#=========================
#
# FUNCTION DEFINITIONS
#
#=========================

def waitForArduino():
    """ wait untill the arduino sends "Arduino is Ready"
    Allows time for arduino reset
    Ensures any bytes left from previous messages are discarded"""

    msg = ""
    while ("Arduino is Ready" in msg) == False:
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

startMarker = ord('<')
endMarker = ord('>')

waitForArduino()

testData = []                                                                    
testData.append("<01234567>")
testData.append("<0x00FF00>")
testData.append("<0x0000FF>")

numLoops = len(testData)
waitingForReply = False

n = 0
while n < numLoops:
    testStr = testData[n]

    if waitingForReply == False:
        # send to arduino
        ser.write(testStr.encode())
        
        print("Test " + str(n) + '\n')
        print("╔═ FROM PC ═══════════════")
        print("║ Sent: " + testStr)
        print("╚═════════════════════════\n")
        
        waitingForReply = True

    if waitingForReply == True:
        while ser.inWaiting() == 0:
            pass
        
        dataRcvd = recvFromArduino()

        print("╔═ FROM ARDUINO ══════════")
        print("║ Received: " + dataRcvd)
        print("╚═════════════════════════\n\n")

        n += 1
        waitingForReply = False
        
#        time.sleep(1)

ser.close
print("Serial port /dev/ttyACM0 closed;\n")


