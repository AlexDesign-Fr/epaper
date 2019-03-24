# This script is a python3 script
#
# ================================================================
import os
import time
import RPi.GPIO as GPIO



# Buttons PIN definitions
Bouton_Meteo    = 36
Bouton_Detail   = 37


GPIO.setmode(GPIO.BOARD)	# We use the board pin number (1 is top left, 2 top right, ...)
GPIO.setup(Bouton_Meteo,    GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO 16 for meteo in INPUT mode
GPIO.setup(Bouton_Detail,   GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO 26 for Detail in INPUT mode



# ________________________________________________________
# Action to execute after a button is pressed
def my_callback(channel):
    time.sleep(0.25)  # Wait a while for the pin to settle (avoid deboucing)

    # Leds animation
    os.system("sudo sh /home/pi/epaper/killClock.sh")

    if( channel == Bouton_Meteo):
    	os.system("sudo python3 /home/pi/epaper/animation.py 45")
        os.system("/home/pi/epaper/meteo.py")

    elif( channel == Bouton_Detail ) :
    	os.system("sudo python3 /home/pi/epaper/animation.py 15")
        os.system("/home/pi/epaper/calendrier.py")

    # restart the clock
    os.system("sudo python3 /home/pi/epaper/clockAllume.py &")



try:
    # see : https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    GPIO.add_event_detect(Bouton_Meteo,     GPIO.RISING, callback=my_callback, bouncetime=1000)  # add rising edge detection on a channel
    GPIO.add_event_detect(Bouton_Detail,    GPIO.RISING, callback=my_callback, bouncetime=1000)  # add rising edge detection on a channel

except KeyboardInterrupt:
    GPIO.cleanup()


# Main loop =================================================
try:  
    while True : pass
except:
    GPIO.cleanup()
