# My take on ambilight
Here's my take on creating an ambilight for my home TV. 
Python does the image aquisition and calculations while the arduino drives the APA102 LEDs.  
(It could eventually do more and better but for now it's working well enough.)

Obligatory screenshot with results.  
\< insert image \>  
avr fps: \< - \> on \< specs \>

******
## Setup
### Hardware
Gear:
- PC
- Arduino
- LEDs
- Power Suply

\< pic \>

### Software
Software: (see **requirements.txt**)
- Python 3
  - mss
  - numpy
  - pyserial

1 Clone this repo

2 **Make sure the TV screen/monitor is 1920x1080p and is the only screen**  
Or...  
2 If you want to try another setup go to **main.py, line 29** and change the screen capture zone.

3 To use simply enter the repo folder and run:
```
python main.py
```
(do not close the terminal)

******
## Python
Functions:  
1. Get screenshot (mss module);
2. Calculate color array (simple average of zone);
3. Send array to Arduino (Serial communication).

## Arduino
Functions:  
1. Receive array from computer (Serial communication);
2. Drive LEDs (FastLED library)

******
TODO:
- [ ] find more accurate way than average for LED color (but still fast, migh try my hands on C/C++)
- [ ] I should try to OOP this thing

