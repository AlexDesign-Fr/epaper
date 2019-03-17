import board
import neopixel


numPixel        = 60
intensite	= 160
pixels 		= neopixel.NeoPixel(board.D18, numPixel)
colBlack	= (0,0,0)

i = 0
while i < numPixel:
	pixels[i]	= colBlack
	i = i +1
