#!/usr/bin/env python
# coding: utf-8

# # Get layout parameters

# read paramenters from params.py
import params as p

# # ./params.py
# # (heigth, length) [cm]
# tvFrame = (56.0, 93.5)
# 
# # (length, height) [cm]
# ledDims = (3.33, 1,0)
# screenFrame = (88.0, 50.0)
# resolution = (1920, 1080)
# 
# # scalar [cm]
# marginOffset = 1.0

# (width, length)
nLEDs = [0,0]
nLEDs[0] = int( p.tvFrame[0] // p.ledDims[0] )

# offset from (left edge, right edge) [cm]
stripOFFSET = [0,0]
stripOFFSET[0] = round( ( p.tvFrame[0] - ( nLEDs[0] * p.ledDims[0] ) ) / 2, 2 )

nLEDs[1] = int( ( p.tvFrame[1] - 2 * ( p.marginOffset + p.ledDims[1] ) ) // p.ledDims[0] )

stripOFFSET[1] = round( ( p.tvFrame[1] - ( nLEDs[1] * p.ledDims[0] ) ) / 2, 2 )

# (length, width) [pixels]
colorZonesDims = [0,0]

colorZonesDims[0] = int( ( p.resolution[0] * p.ledDims[0] ) / p.screenFrame[0] )
colorZonesDims[1] = int( ( p.resolution[1] - ( colorZonesDims[0] * ( nLEDs[0] - 2 ) ) ) / 2 )

# scalar [pixels]
pixelOFFSET = int( ( p.resolution[0] - ( nLEDs[1] * colorZonesDims[0] ) ) / 2 )

print("LED count                           :", nLEDs, "LEDs   - [left/right, top/bottom] rows"                                   )
print("LED strip offset                    :", stripOFFSET, "cm - from [left/right, top/bottom] tv frame\n"                      )
print("color zones dimensions              :", colorZonesDims, "pixels - [length, width], switched from top/bottom to left/right")
print("top/bottom color zones pixel offset :", pixelOFFSET, "pixels       - from [left/right] in top/bottom row of color zones"  )




