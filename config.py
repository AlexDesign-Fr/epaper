# ======================================================================================================================
# Define here all the Google agenda you want to display
# In Google agenda, each calendar is defined by it's ID (right click on a calendar name, select "Settings" and look for "Calendar's ID"
CalendarsID = ["YourGoogleAgendaIDHere",
                 "#contacts@group.v.calendar.google.com"]



# ======================================================================================================================
# If modifying the scopes, delete the file token.json.
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
scopes      = 'https://www.googleapis.com/auth/calendar.readonly'


# ======================================================================================================================
# Your Domoticz instance. ( https://www.domoticz.com/wiki/Main_Page )
# If you don't have any Domoticz instance, just let it blanck.
# This request stand to display thermometers temperature stored in Domoticz.
# Domoticz_externalThermometreIDx is a thermometer standing outside. If it's not set, the temperature coming from Openweather
# will be displayed.
Domoticz_ServerIP               = "192.168.0.1"
Domoticz_ServerPort             = "80"
Domoticz_UserName               = "YourUserName"
Domoticz_Password               = "YourUserPassword"
Domoticz_externalThermometreIDx = "99"
Domoticz_url                    = "http://"+Domoticz_ServerIP+":"+Domoticz_ServerPort+"/json.htm?username="+Domoticz_UserName+"&password="+Domoticz_Password+"&type=devices&filter=temp&used=true&order=Name"



# ======================================================================================================================
# Open weather API.
# You have to create an account to https://home.openweathermap.com/ and then define an API key in
# https://home.openweathermap.org/api_keys
openWeatherAPI      = "yourOpenWeatherAPIKeyHere"
openWeatherCityName = "2986991"
