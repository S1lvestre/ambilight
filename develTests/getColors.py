import mss
import numpy as np

numLEDS = 84
zonesCount = [26, 16]    # top/bottom, left/right
zonesDism = [72, 36, 24] # length, width, offset

# Part of the screen to capture
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

##################################
#
# FUNCTIONS
#
##################################

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




##################################
#
# MAIN
#
##################################

with mss.mss() as sct:

#   while True:
    
    goingOut = "<"

        # Get raw pixels from the screen, save it to a Numpy array
    img = np.array(sct.grab(monitor))[:,:,:3]
    
    # top row
    for top_i in range(zonesCount[0]) :
        zone = img[0:36, (72*top_i)+24 : (72*(top_i+1))+24]
        avrgColor = calcAvrg(zone)
        goingOut += rgbToStr(avrgColor)
    
    #top right
    zone = img[0:36, -36:1920]
    avrgColor = calcAvrg(zone)
    goingOut += rgbToStr(avrgColor)

    # right row
    for right_i in range(zonesCount[1]-2):
        zone = img[(72*right_i)+36 : (72*(right_i+1))+36 , -36:1920 ]
        avrgColor = calcAvrg(zone)
        goingOut += rgbToStr(avrgColor)
    
    #bot right
    zone = img[-36:1080, -36:1920]
    avrgColor = calcAvrg(zone)
    goingOut += rgbToStr(avrgColor)

    # bottom row
    for bot_i in range(zonesCount[0]) :
        zone = img[-36:1080, (72*bot_i)+24 : (72*(bot_i+1))+24  ]
        avrgColor = calcAvrg(zone) 
        goingOut += rgbToStr(avrgColor)
    
    #bot left
    zone = img[-36:1080, 0:36]
    avrgColor = calcAvrg(zone)
    goingOut += rgbToStr(avrgColor)

    # left row
    for left_i in range(zonesCount[1]-2):
        zone = img[(72*left_i)+36 : (72*(left_i+1))+36 , 0:36 ]
        avrgColor = calcAvrg(zone)
        goingOut += rgbToStr(avrgColor)

    #top left
    zone = img[0:36, 0:36]
    avrgColor = calcAvrg(zone)
    goingOut += rgbToStr(avrgColor)


    goingOut += '>'
    print(goingOut)






























