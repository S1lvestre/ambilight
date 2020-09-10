# My take on ambilight
******
Here's my take on creating an ambilight for my home TV. 
Python does the image aquisition and calculations while the arduino drives the APA102 LEDs.

Obligatory screenshot with results.
\< insert image \>
avr fps: \< - \> on \< specs \>

##Setup
******
###Hardware
Gear:
- PC
- Arduino
- LEDs
- Power Suply

\< pic \>

###Software
Clone this repo, enter it and run
"""
python main.py
"""

**As of now, make sure the TV screen/monitor is 1920x1080p and is the only screen.** Or...

If you want to try another setup go to *main.py, line 29* and change the screen capture zone.

******
## Python
Functions:  
- Get screenshot (mss module);
- Calculate color array (simple average of zone);
- Send array to Arduino (Serial communication).

## Arduino
Functions:  
- Receive array from computer (Serial communication);
- Drive LEDs (FastLED library)

TODO:
- [ ] find more accurate way than average for LED color (but still fast, migh try my hands on C/C++)
- [ ] I should try to OOP this thing

