#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
import os
import traceback
from PIL import Image,ImageDraw,ImageFont

# Modify PYTHONPATH for local libs
os.putenv("PYTHONPATH", os.path.normpath(os.path.dirname( __file__ )))
import libs.epd7in5 as epd7in5



# Actual date ==========================================================================================================
now = datetime.now()




# Test if we have a picture to display today ===========================================================================
directoryContent    = os.listdir(os.path.dirname(os.getcwd()+"/photos/"))
dateFichier         = str('{:02d}'.format(now.day))+str('{:02d}'.format(now.month))
fileToDisplay       = ""

for fileName in directoryContent:

    # if the imagename start with today date
    # to display a picture for the 31th of December (12th month), the filename should begin with 3112
    if( fileName[:4] == dateFichier) :
        fileToDisplay = fileName



# If we found a file to display ========================================================================================
if( fileToDisplay != ""):
    try:
        # initialise the screen
        epd = epd7in5.EPD()
        epd.init()
        epd.Clear(0xFF)
        screenHeight    = epd7in5.EPD_WIDTH
        screenWidth     = epd7in5.EPD_HEIGHT


        # Display the picture
        pictureCompletName = os.path.dirname(os.getcwd()+"/photos/")+"/"+fileToDisplay
        print("Display picture :"+pictureCompletName)
        Limage      = Image.open(pictureCompletName)
        epd.display(epd.getbuffer(Limage))


        # Set the screeen to sleep mode
        epd.sleep()
    except:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        exit()

