import serial
import time

startMarker = ord('<')
endMarker = ord('>')



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

waitForArduino()

testData = []
#testData.append("<01234567;>")
testData.append("<0x000000;0x000000;0x000000;>")
testData.append("<0x111111;0x111111;0x111111;>")
testData.append("<0x222222;0x222222;0x222222;>")
testData.append("<0x333333;0x333333;0x333333;>")
testData.append("<0x444444;0x444444;0x444444;>")
testData.append("<0x555555;0x555555;0x555555;>")
testData.append("<0x666666;0x666666;0x666666;>")
testData.append("<0x777777;0x777777;0x777777;>")
testData.append("<0x888888;0x888888;0x888888;>")
testData.append("<0x999999;0x999999;0x999999;>")
testData.append("<0xAAAAAA;0xAAAAAA;0xAAAAAA;>")
testData.append("<0xBBBBBB;0xBBBBBB;0xBBBBBB;>")
testData.append("<0xCCCCCC;0xCCCCCC;0xCCCCCC;>")
testData.append("<0xDDDDDD;0xDDDDDD;0xDDDDDD;>")
testData.append("<0xEEEEEE;0xEEEEEE;0xEEEEEE;>")
testData.append("<0xFFFFFF;0xFFFFFF;0xFFFFFF;>")
testData.append("<0xEEEEEE;0xEEEEEE;0xEEEEEE;>")
testData.append("<0xDDDDDD;0xDDDDDD;0xDDDDDD;>")
testData.append("<0xCCCCCC;0xCCCCCC;0xCCCCCC;>")
testData.append("<0xBBBBBB;0xBBBBBB;0xBBBBBB;>")
testData.append("<0xAAAAAA;0xAAAAAA;0xAAAAAA;>")
testData.append("<0x999999;0x999999;0x999999;>")
testData.append("<0x888888;0x888888;0x888888;>")
testData.append("<0x777777;0x777777;0x777777;>")
testData.append("<0x666666;0x666666;0x666666;>")
testData.append("<0X555555;0X555555;0X555555;>")
testData.append("<0x444444;0x444444;0x444444;>")
testData.append("<0x333333;0x333333;0x333333;>")
testData.append("<0x222222;0x222222;0x222222;>")
testData.append("<0x111111;0x111111;0x111111;>")
testData.append("<0x000000;0x000000;0x000000;>")

numLoops = len(testData)
waitingForReply = False

for i in range(3) :
    n = 0
    while n < numLoops:
        testStr = testData[n]
        
        if waitingForReply == False:
            # send to arduino
            ser.write(testStr.encode())
            
            print("Test " + str(n) + '\n')
            print("╔═══════ PC ══════════════")
            print("║     Sent: " + testStr)
            print("╚═════════════════════════\n")
            
            n += 1
            time.sleep(.1)
            #waitingForReply = True
        
        if waitingForReply == True:
            while ser.inWaiting() == 0:
                pass
            
            dataRcvd = recvFromArduino()
            
            print("╔══ ARDUINO ══════════════")
            print("║ Received:  " + dataRcvd)
            print("╚═════════════════════════\n\n")
    
            #n += 1
            #waitingForReply = False
            
            #time.sleep(.1)

ser.close
print("Serial port /dev/ttyACM0 closed;\n")


