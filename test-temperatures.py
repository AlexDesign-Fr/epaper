#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json
import config

# Recupere toutes les temperatures mesurées dans Domoticz
url     = config.Domoticz_url
xml     = requests.get(url)
data    = xml.json()

# thermometre list
thermometres = data['result']



print( thermometres)
for thermometre in thermometres:
    print(thermometre['Name'])
    print("{:.2f}°C" .format(thermometre['Temp']))
    try:
        print("{:.2f} %".format(thermometre['Humidity']))
    except:
        print("")