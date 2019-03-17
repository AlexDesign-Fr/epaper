#!/usr/bin/python
# -*- coding:utf-8 -*-
# @see https://developers.google.com/calendar/quickstart/python


from __future__ import print_function
import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import config

# ======================================================================================================================
# Define here all the Google agenda you want to display
# In Google agenda, each calendar is defined by it's ID (right click on a calendar name, select "Settings" and look for "Calendar's ID"
g_CalendarsID = config.CalendarsID
g_scopes      = config.scopes


# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', g_scopes)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
l_TAB_Events  = []
for calendarID in g_CalendarsID:
    events_result = service.events().list(calendarId=calendarID, timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
    events  = events_result.get('items', [])
    l_TAB_Events.append(events)




# recuperation des anniversaires et des rendez-vous
l_TAB_Birthdays   = []
l_TAB_RendezVous  = []
for events in l_TAB_Events:
    for event in events:
        start   = event['start'].get('dateTime', event['start'].get('date'))
        date   = start.split('T')

        # we got a birthday
        if("Anniversaire") in event['summary']:
            date    = start.split("-")
            #name    = event['summary'][13:]
            name    = event['summary'].replace(" - Anniversaire", "")
            name    = name.replace("Anniversaire ", "")

            l_TAB_Birthdays.append([name, date[2], date[1]])

        # we got an event
        else:
            temp    = start.split("T")  # ['2019-01-04', '13:00:00+01:00']
            date    = temp[0].split("-")
            l_TAB_RendezVous.append([event['summary'], date[2], date[1], date[0], temp[1][:5]])


print(l_TAB_Birthdays)
print(l_TAB_RendezVous)

for annif in l_TAB_Birthdays:
    print(annif)
