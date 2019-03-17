import board
import neopixel
from datetime import datetime
import time
import os
import psutil


numPixel	= 60
pixels 		= neopixel.NeoPixel(board.D18, numPixel)
colBlack	= (0,0,0)


# Save the PID in a file =========================================================
def writePidFile():
  # Before to start, we kill all the old instance
  try:
    with open('/tmp/clock_pid') as f:
      pids = f.read().splitlines() # read all the saved pids from file

    for pid in pids:
      # try to kill the process one by one
      try:
        p = psutil.Process(int(pid))
        p.kill()
      except : pass
  except: pass

  # there are no more instance, so we can save the present pid for nexte instance
  pid = str(os.getpid())
  f = open('/tmp/clock_pid', 'a')
  f.write(pid+"\n")
  f.close()


# LEDs animation to "clean" the strp led =========================================
def animation():
	ecart = 255
	i = 0
	while i < numPixel:
		color = int(ecart * i / numPixel)
		pixels[i]	= (color, 0, 255 - color)
		time.sleep(0.001)
		i = i +1

	i = 0
	while i < numPixel:
		pixels[i]	= colBlack
		time.sleep(0.001)
		i = i +1





# Main programm ==================================================================
writePidFile()
while True:
	now	= datetime.now()
	# Luminosity ----------------------
	if( now.hour > 9) and(now.hour < 21):
		intensite = 255
	else:
		intensite = 5
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

	if( now.second == 0 ):
		animation()

	# Reset last time ----------------------
	pixels[now.second -1]	= colBlack



	# Display current time ----------------------
	pixels[now.second]	= colSeconde
	pixels[now.minute % 60]	= colMinute
	pixels[hour] 		= colHour


	time.sleep(0.5)
