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
testData.append("<0x000000>")
testData.append("<0x111111>")
testData.append("<0x222222>")
testData.append("<0x333333>")
testData.append("<0x444444>")
testData.append("<0x555555>")
testData.append("<0x666666>")
testData.append("<0x777777>")
testData.append("<0x888888>")
testData.append("<0x999999>")
testData.append("<0xAAAAAA>")
testData.append("<0xBBBBBB>")
testData.append("<0xCCCCCC>")
testData.append("<0xDDDDDD>")
testData.append("<0xEEEEEE>")
testData.append("<0xFFFFFF>")
testData.append("<0xEEEEEE>")
testData.append("<0xDDDDDD>")
testData.append("<0xCCCCCC>")
testData.append("<0xBBBBBB>")
testData.append("<0xAAAAAA>")
testData.append("<0x999999>")
testData.append("<0x888888>")
testData.append("<0x777777>")
testData.append("<0x666666>")
testData.append("<0X555555>")
testData.append("<0x444444>")
testData.append("<0x333333>")
testData.append("<0x222222>")
testData.append("<0x111111>")
testData.append("<0x000000>")

numLoops = len(testData)
waitingForReply = False

for i in range(5) :
    n = 0
    while n < numLoops:
        testStr = testData[n]
        
        if waitingForReply == False:
            # send to arduino
            ser.write(testStr.encode())
            
            print("Test " + str(n) + '\n')
            print("╔═ PC ════════════════════")
            print("║     Sent: " + testStr)
            print("╚═════════════════════════\n")
            
            waitingForReply = True
        
        if waitingForReply == True:
            while ser.inWaiting() == 0:
                pass
            
            dataRcvd = recvFromArduino()
            
            print("╔═ ARDUINO ═══════════════")
            print("║ Received:  " + dataRcvd)
            print("╚═════════════════════════\n\n")
    
            n += 1
            waitingForReply = False
            
            time.sleep(.1)

ser.close
print("Serial port /dev/ttyACM0 closed;\n")


