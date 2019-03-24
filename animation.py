# This python script is a python3 script
#
# ================================================================
from datetime import datetime
import time
import board
import neopixel
import sys

# Neopixels definitions
numPixel    = 60
intensite   = 255
pixels      = neopixel.NeoPixel(board.D18, numPixel)	# PIN18 (GPIO24)
colBlack    = (0,0,0)
colGreen    = (0,intensite,0)


# ________________________________________________________
# Leds animations to indicate a button have been pressed
def animation( start ):

	i      = 0
	middle	= int( start )
	# Green animation, starting from "middle" pixel number
	while i < numPixel /2 :
		pixels[(middle + i) % numPixel]   = colGreen
		pixels[(middle - i) % numPixel]   = colGreen
		time.sleep(0.01)
		i = i +1

	i = 0
	# turn off the leds
	while i < numPixel /2 :
		pixels[(middle + i) % numPixel]   = colBlack
		pixels[(middle - i) % numPixel]   = colBlack
		time.sleep(0.01)
		i = i +1



# ________________________________________________________
# Display the current time on the leds trip
def displayClock():
	# Display the led's clock
	now = datetime.now()
	colHour            = (intensite,0,0)	# Red
	colMinute          = (intensite,intensite,intensite)	# White
	colSeconde         = (int(intensite/10),int(intensite/10),int(intensite/10)) # Grey

	# Hour led position  ----------------------
	if( now.hour > 12 ):
		hour	= int((now.hour -12) * 60/12)
	elif (now.hour == 12):
		hour	= 59
	else:
		hour	= int(now.hour * 60/12)

	# Display current time ----------------------
	pixels[now.second]	= colSeconde
	pixels[now.minute % 60]	= colMinute
	pixels[hour] 		= colHour





# Main loop =================================================
# Read arguments found in command line
# sys.argv[0] is the programme name
if( len(sys.argv) == 1 ):
	PixelNumberBegining	= 30
else:
	PixelNumberBegining = int(sys.argv[1])

animation(PixelNumberBegining)
displayClock()
