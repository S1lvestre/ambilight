import time
import mss
import cv2
import numpy as np

def avg(img):
    return np.mean(img, axis=(0,1)) # (blue, green, red)

# Get raw pixels from the screen, save it to a Numpy array
#img = np.array(cv2.imread('red-background.jpg'))
with mss.mss() as sct:

    bgr = np.zeros((4,), dtype=int)
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    while "Screen capturing":

        last_time = time.time()

    	# Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        bgr = avg(img)

        print(bgr.astype(int)) # *floor not round 

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

	



	


