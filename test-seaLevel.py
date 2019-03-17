#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
import traceback
from datetime import timedelta

from bleach import clean
import requests
import requests_cache



# Setting up a cache for requests (TTL = 15 minutes) ===================================================================
requests_cache.install_cache('opeWeatherCache', expire_after=timedelta(minutes=15))


# SEA LEVEL ============================================================================================================
# Pour récupérer l'ID d'un port, il faut aller sur http://maree.info/75
port    = 74
url     = "http://horloge.maree.frbateaux.net/ws" + str(port) + ".js?col=1&c=0"
content = requests.get(url)

print(content.text)
print("---------------------------")
try:
    # Basse et pleine mer
    temp    = content.text.split("PMBM")

    chaine  = temp[2].split("=\"")
    # Clean HTML tags
    complet = clean(chaine[1], tags=[], strip=True, strip_comments=True)
    temp    = complet.split("BM ")
    bassMer     = temp[1][:5]

    temp = complet.split("PM ")
    pleineMer   = temp[1][:5]


except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    print("********** probleme lors de l'extraction des heures de marée de la chaine *************")
    print(content.text)
    bassMer     = ""
    pleineMer   = ""
try:
    # Coefficient
    temp = content.text.split("Coef.")
    temp = temp[1].split("<br>")
    temp = temp[1].split("\"")
    coeffMaree = temp[0]
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    print("********** probleme lors de l'extraction du coeff. de marée de la chaine *************")
    print(content.text)
    coeffMaree = ""


print( coeffMaree, pleineMer, bassMer)