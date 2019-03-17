#!/usr/bin/python
# -*- coding:utf-8 -*-

# Init the screen ======================================================================================================
try:
    epd = epd7in5.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the Vertical image ("portrait" mode)
    screenHeight = epd7in5.EPD_WIDTH
    screenWidth = epd7in5.EPD_HEIGHT
    Limage = Image.new('1', (screenWidth, screenHeight), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)

    # Fonts
    font10 = ImageFont.truetype('/home/pi/epaper/font/ForcedSquare.ttf', 10)
    font12 = ImageFont.truetype('/home/pi/epaper/font/CaviarDreams.ttf', 12)
    font15 = ImageFont.truetype('/home/pi/epaper/font/KeepCalm-Medium.ttf', 15)
    font17 = ImageFont.truetype('/home/pi/epaper/font/KeepCalm-Medium.ttf', 17)
    font30 = ImageFont.truetype('/home/pi/epaper/font/KeepCalm-Medium.ttf', 30)
    fontFixe = ImageFont.truetype('/home/pi/epaper/font/CQ_Mono.otf', 20)
    fontJourChiffre = ImageFont.truetype('/home/pi/epaper/font/gomarice_goma_block.ttf', 90)
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()




# Setting up a cache for requests (TTL = 15 minutes) ===================================================================
requests_cache.install_cache('opeWeatherCache', expire_after=timedelta(minutes=15))



# Actual date ==========================================================================================================
now = datetime.now()
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
calendar.setfirstweekday(calendar.MONDAY)  # First day of week is set to "monday"
l_TAB_Jours = calendar.day_name
l_TAB_Mois  = calendar.month_name




# Domoticz =============================================================================================================
g_Domoticz_url                      = config.Domoticz_url
g_Domoticz_externalThermometreIDx   = config.Domoticz_externalThermometreIDx
try:
    xml     = requests.get(g_Domoticz_url)
    if( xml.status_code == requests.codes.ok ): # Request is OK
        data    = xml.json()
        # thermometre list
        thermometres = data['result']

    else:
        thermometres = []


except:
    thermometres = []









# WEATHER CONDITION (and forcast) ======================================================================================
# icone du temps (see https://openweathermap.org/weather-conditions )
weather     = requests.get("http://api.openweathermap.org/data/2.5/weather?id="+config.openWeatherCityName+"&units=metric&appid="+config.openWeatherAPI)
forecast    = requests.get("http://api.openweathermap.org/data/2.5/forecast?id="+config.openWeatherCityName+"&units=metric&appid="+config.openWeatherAPI)
weatherActualCondition  = weather.json()
weatherForcast          = forecast.json()
weatherForcast          = weatherForcast['list']

def ConvertTimeStamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d %Hh')







# SEA LEVEL ============================================================================================================
# Pour récupérer l'ID d'un port, il faut aller sur http://maree.info/75
port = 74
url = "http://horloge.maree.frbateaux.net/ws" + str(port) + ".js?col=1&c=0"
content = requests.get(url)
try:
    # Basse et pleine mer
    temp = content.text.split("PMBM")

    chaine = temp[2].split("=\"")
    # Clean HTML tags
    complet = clean(chaine[1], tags=[], strip=True, strip_comments=True)
    temp = complet.split("BM ")
    bassMer = temp[1][:5]

    temp = complet.split("PM ")
    pleineMer = temp[1][:5]
except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    print("********** probleme lors de l'extraction des heures de marée de la chaine *************")
    print(content.text)
    bassMer = ""
    pleineMer = ""

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







def AfficheLigneText(text, x, y, maxCaract):
    draw.text((x, y), text[:maxCaract], font=font10, fill=0)
    draw.text((x, y +10), text[maxCaract:], font=font10, fill=0)









# Display the header ===================================================================================================
try:

    # Day --------------------------------------------------------------
    draw.rectangle((0, 0, screenWidth, 140), fill=0)  # black rectangle
    if (now.day < 10):
        day = "0" + str(now.day)
    else:
        day = str(now.day)

    if (len(l_TAB_Mois[now.month - 1]) < 8):
        month = l_TAB_Mois[now.month].title() + " " + str(now.year)
    else:
        month = l_TAB_Mois[now.month].title()

    # Suppression des caractères accentués dans le mois
    month = unicode(month, 'utf-8')
    month = unicodedata.normalize('NFD', month).encode('ascii', 'ignore')

    # Affichage du jour & mois
    draw.text((7, 3), l_TAB_Jours[now.weekday()].title(), font=font17, fill=255)
    draw.text((5, 15), day, font=fontJourChiffre, fill=255)
    draw.text((7, 100), month, font=font17, fill=255)

    # Meteo icon -------------------------------------------------------
    try:
        conditionText = weatherActualCondition['weather'][0]['main']
        conditionTemp = str("%.1f" % weatherActualCondition['main']['temp']) + "°C"[1:]
        temperatureMin = "min " + str("%.1f" % weatherActualCondition['main']['temp_min']) + " C"
        temperatureMax = " max " + str("%.1f" % weatherActualCondition['main']['temp_max']) + " C"

    except:
        print('traceback.format_exc():\n%s', traceback.format_exc())
        conditionText = ""
        conditionTemp = ""
        temperatureMin = ""
        temperatureMax = ""

    iconeFile = '/home/pi/epaper/icones/' + weatherActualCondition['weather'][0]['icon'] + '.bmp'
    # if icone exist, we display it, textual weather condition otherwith
    if (os.path.isfile(iconeFile)):
        iconeMeteo = Image.open(iconeFile)
        Limage.paste(iconeMeteo, (140, 0))  # Coin haut gauche de l'image
    else:
        draw.text((130, 50), conditionText, font=font15, fill=255)

    # Temperature ------------------------------------------------------
    # In case of Domoticz was  not responding before ...
    # We take the outside temperature
    externalTemp = conditionTemp
    trouve = False
    for thermometre in thermometres:
        if (thermometre['idx'] == g_Domoticz_externalThermometreIDx):
            externalTemp = str(thermometres[2]['Temp']) + "°C"[1:]
            trouve = True

    if (not trouve):
        draw.text((10, 180), "Aucun thermometres accessible ...", font=font17, fill=0)

    draw.text((280, 5), externalTemp, font=font30, fill=255)
    draw.text((280, 35), temperatureMin + temperatureMax, font=font12, fill=255)

    # Sea levels -------------------------------------------------------
    icoSeaLevelUp = Image.open('/home/pi/epaper/icones/seaLevelUp.bmp')
    icoSeaLevelDown = Image.open('/home/pi/epaper/icones/seaLevelDown.bmp')
    draw.text((280, 50), "Coeff. " + str(coeffMaree), font=font15, fill=255)
    Limage.paste(icoSeaLevelUp, (280, 70))  # Coin haut gauche de l'image
    draw.text((320, 75), str(pleineMer), font=font15, fill=255)

    Limage.paste(icoSeaLevelDown, (280, 95))  # Coin haut gauche de l'image
    draw.text((320, 100), str(bassMer), font=font15, fill=255)

    # Meteo forcast ----------------------------------------------------
    # We display only 12 next forcasts
    X = 0
    Y = 120
    for forcast in weatherForcast[:12]:
        # Icone (32x28)
        iconeMeteo = Image.open('/home/pi/epaper/icones/' + forcast['weather'][0]['icon'] + '_small.bmp')
        Limage.paste(iconeMeteo, (X, Y + 6))  # Coin haut gauche de l'image

        # Date + time
        textMeteo = ConvertTimeStamp(forcast['dt'])
        draw.text((X + 2, Y - 1), str(textMeteo), font=font10, fill=255)

        X = X + 32  # icon width
    # Horizontal line
    Y = Y + 33
    draw.line((0, Y, screenWidth, Y), fill=0)

    # Températures (Domoticz) ------------------------------------------
    X = 20
    Y = 160
    icoTemperatur = Image.open('/home/pi/epaper/icones/thermometre.bmp')
    icoHumidity = Image.open('/home/pi/epaper/icones/humidity.bmp')
    for thermometre in thermometres:

        # Display every thermometers except those for outside
        if (thermometre['idx'] != g_Domoticz_externalThermometreIDx):
            # Clear space
            draw.rectangle((X, Y, X + 90, Y + 60), fill=255)

            # Temperature
            temperature = "{:.1f}".format(thermometre['Temp']) + "°C"[1:]
            Limage.paste(icoTemperatur, (X, Y))  # Coin haut gauche de l'image
            draw.text((X + 15, Y), temperature, font=font17, fill=0)

            # Humidity (if exist)
            try:
                humidity = "{:.0f} %".format(thermometre['Humidity'])
                Limage.paste(icoHumidity, (X, Y + 23))  # Coin haut gauche de l'image
            except:
                humidity = ""

            draw.text((X + 15, Y + 20), humidity, font=font17, fill=0)

            # Thermometre Name
            AfficheLigneText(thermometre['Name'], X, Y + 40, 16)

            # Vertical line
            draw.line((X + 83, Y - 5, X + 83, Y + 65), fill=0)

            X = X + 90

    # delete last vertical line
    X = X - 90
    draw.line((X + 83, Y - 5, X + 83, Y + 65), fill=255)



except:
    print('traceback.format_exc():\n%s', traceback.format_exc())
    exit()