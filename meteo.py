#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from PIL import Image, ImageDraw, ImageFont
import traceback
from datetime import datetime
from datetime import timedelta
import unicodedata

import config

import os
import calendar
import locale
from bleach import clean
import requests
import requests_cache



# Modify PYTHONPATH for local libs
os.putenv("PYTHONPATH", os.path.normpath(os.path.dirname(__file__)))
import libs.epd7in5 as epd7in5



# Diaplsy common informations (date, forecast, sea level, ... ==========================================================
execfile("bandeauHaut.py")


try:
    # Meteo forcast ----------------------------------------------------
    Pos_Temperature = 90
    Pos_Wind        = 190
    Pos_Description = 245
    Y = Y + 70

    # Header
    draw.text((35,Y),"Jour, Heure", font=font10, fill=0)
    draw.text((Pos_Temperature, Y), "Temp., (min/max)", font=font10, fill=0)
    draw.text((Pos_Wind, Y), "Vitesse vent", font=font10, fill=0)
    draw.text((Pos_Description, Y), "Description", font=font10, fill=0)

    # We display only the 15'e first lines from Open Weather forcast
    for forcast in weatherForcast[:15]:
    	X = 0
        # Icone (32x28)
        iconeMeteo = Image.open('/home/pi/epaper/icones/' + forcast['weather'][0]['icon'] + '_small.bmp')
        Limage.paste(iconeMeteo, (X, Y))  # Coin haut gauche de l'image

        # Date + time
        dateTime = ConvertTimeStamp(forcast['dt'])
        draw.text((X + 35, Y +10), str(dateTime), font=font12, fill=0)

        # temperatures
        temperatures	= str(forcast['main']['temp'])+ "°C"[1:]
        minMax	= " ("+ str(forcast['main']['temp_min'])[:3] +"/"+ str(forcast['main']['temp_max'])[:3] +")"
        draw.text((Pos_Temperature , Y+10), temperatures + minMax, font=font12, fill=0)

        # Wind speed
        windSpeed	= str(forcast['wind']['speed']) + " m/s"
        draw.text((Pos_Wind , Y+10), windSpeed, font=font12, fill=0)

        # Description
        description = forcast['weather'][0]['description']
        draw.text((Pos_Description, Y+10), description, font=font12, fill=0)
	

        Y = Y + 30  # icon width
	

	# Draw an horizontal line
	draw.line((0, Y -2, screenWidth, Y -2), fill=0)

















    # Last update ------------------------------------------------------
    upDate = "Le " + str(now.day) + " a " + str(now.hour) + ":" + str(now.minute)
    draw.text((X, Y + 3), upDate, font=font10, fill=0)



    # Update Screen ----------------------------------------------------
    epd.display(epd.getbuffer(Limage))
    epd.sleep()




except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()

