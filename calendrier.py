#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime
from datetime import timedelta
import unicodedata

import os
import calendar
import config
import locale
from bleach import clean
import requests
import requests_cache



from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# Modify PYTHONPATH for local libs
os.putenv("PYTHONPATH", os.path.normpath(os.path.dirname( __file__ )))
import libs.epd7in5 as epd7in5



# ======================================================================================================================
# Define here all the Google agenda you want to display
# In Google agenda, each calendar is defined by it's ID (right click on a calendar name, select "Settings" and look for "Calendar's ID"
g_CalendarsID = config.CalendarsID
g_scopes      = config.scopes







# Displsy common informations (date, forecast, sea level, ... ==========================================================
execfile("bandeauHaut.py")



# Birthdays (from google agenda) =======================================================================================
icoBirthdaySmall= Image.open("/home/pi/epaper/icones/birthday_small.bmp")
icoBirthdayBig  = Image.open("/home/pi/epaper/icones/Birthday.bmp")
icoEvent        = Image.open("/home/pi/epaper/icones/event.bmp")
icoTrashbin     = Image.open("/home/pi/epaper/icones/trashbin.bmp")

# Array containing all the Birthdays found in Google Agenda, Genarally "#contacts@group.v.calendar.google.com""
l_TAB_Birthdays   = []

# Array containing all the Events found in Google Agenda
l_TAB_RendezVous  = []


def RecupeAgenda(scopes, CalendarsID):
    # If modifying these scopes (see config.py file), delete the file token.json.
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    myCalendarsID = CalendarsID
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    l_TAB_Events = []
    for calendarID in myCalendarsID:
        events_result = service.events().list(calendarId=calendarID, timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        l_TAB_Events.append(events)

    # Extract  Birthdays and Events from google agenda
    for events in l_TAB_Events:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            # we got a birthday
            if ("Anniversaire") in event['summary']:
                date = start.split("-")
                # name    = event['summary'][13:]
                name = event['summary'].replace(" - Anniversaire", "")
                name = name.replace("Anniversaire ", "")

                l_TAB_Birthdays.append([name, int(date[2]), int(date[1])])

            # we got an event
            else:
                # sometime, the starting date is in short format (2019-04-13) because there is no time set
                # (this is the case for some event longer  than 24 hours)
                if ("T" in start):
                    temp = start.split("T")  # ['2019-01-27', '13:00:00+01:00']

                else:
                    temp = [start, "00:00:00+00:00"]

                date = temp[0].split("-")
                # Store data as ["summary, day, month, year, hh:mm:ss]
                l_TAB_RendezVous.append([event['summary'], int(date[2]), int(date[1]), int(date[0]), temp[1][:5]])


# Display the calendar =================================================================================================
try :

    # Calendar ---------------------------------------------------------
    RecupeAgenda(g_scopes, g_CalendarsID)
    X = 0
    Y = Y + 70
    X_Step  = screenWidth / 7
    Y_Step  = 60
    for day in l_TAB_Jours:
        draw.text((X +2, Y), str(day.title()[:3]), font=fontFixe, fill=0)
        X = X + X_Step
    
    X = 0
    Y = Y +30
    monthCalendar   = calendar.monthcalendar(now.year,now.month)
    for week in monthCalendar:
        column   = 1
        for day in week:
            # Number of the day
            if( day != 0 ):
                draw.text((X +5, Y), str(day), font=fontFixe, fill=0)
                
                # box around the number
                draw.rectangle((X, Y, X + (X_Step), Y + Y_Step), outline=0)
                
                # if it's a past day, cross it
                if( day < now.day ):
                    draw.line((X, Y, X +X_Step, Y +Y_Step), fill=0)
                    draw.line((X +X_Step, Y, X, Y +Y_Step), fill=0)
                
                # if it's a birthday
                posY    = Y
                for birthday in l_TAB_Birthdays:
                    if (birthday[1]  == day) and (birthday[2] == now.month):
                        # icone
                        Limage.paste(icoBirthdaySmall,(X +X_Step-8,Y-10))
                        
                        # Name
                        draw.text((X +3, posY+17), birthday[0][:10], font=font10, fill=0)
                        posY    = posY + 17
                
                # it's an event
                for event in l_TAB_RendezVous:
                    if (event[1]  == day) and (event[2] == now.month):
                        # icone
                        if( event[0] == "Sortir la poubelle" ) :
                            # trashbin icon
                            Limage.paste(icoTrashbin, (X +X_Step - 20,Y-4))
                        else :
                            Limage.paste(icoEvent, (X + X_Step - 16, Y - 4))

                        # Name
                        draw.text((X +4, posY+17), event[0][:10], font=font10, fill=0)
                        draw.text((X +4, posY+17+7), event[0][10:], font=font10, fill=0)

                        posY    = posY + 17

            
            X       = X + X_Step
            column  = column +1
            
        Y = Y + Y_Step
        X = 0
        
    


    # Last update ------------------------------------------------------
    upDate  = "Le " +str(now.day) +" a "+ str(now.hour) +":"+ str(now.minute)
    draw.text((X,Y+3), upDate, font=font10, fill=0)




    # Incoming events  ---------------------------------------------------
    X = 0
    Y = screenHeight
    for event in reversed(l_TAB_RendezVous):
        # today's event
        if( event[1] == now.day ):
            Y   = Y -15
            chaine    = event[4] + " " + event[0]
            draw.text((X, Y), chaine, font=font15, fill=0)
        
        # other event (I prefer icone's than recurrent event, so if the event is reconized here, we display the appropriate icon)
        else:
            if (event[0] != "Sortir la poubelle") :
                Y   = Y -12
                chaine    = str(event[1]) + "/" + str(event[2]) + " " + event[4] + ": " + event[0]
                draw.text((X, Y), chaine, font=font12, fill=0)

    





    # Birthday revue ---------------------------------------------------
    # We display  all the birday's in the bottom right corner of the screen
    # If we found a birthday for today, we display a big cake !
    X = (screenWidth / 2) + 90
    
    # Vertical line
    draw.line((X-5,Y, X-5, screenHeight), fill=0)
    
    Y = screenHeight
    existBirthday = 0
    for birthday in l_TAB_Birthdays:
        if (birthday[2] == now.month):
            Y   = Y -12
            
            # Name
            annif   = birthday[0]
            draw.text((X, Y), annif, font=font12, fill=0)

            # If there is a birthday today
            if( birthday[1] == now.day):
                existBirthday = 1
            
    # Picture (birdthay cake)
    if( existBirthday == 1):
        Limage.paste(icoBirthdayBig,(screenWidth -57,Y -80))








    # Update the screen -----------------------------------------------
    epd.display(epd.getbuffer(Limage))
    epd.sleep()




except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()

