# epaper
Utilisation d'un écran epaper pour afficher un Google Agenda + prévision météo + météo locale + température Domoticz

Please refer to https://www.alex-design.fr/Projets-R-A/Calendrier-epaper for (french) usage


There are several Python programs that are used in this project. They are either launched by the main program or by a cron job or by an external event.

The main program (main.py) is started when the raspberry is started. It runs in a loop and calls the display programs when pressed buttons.

Every hour a cron job will refresh the calendar.

Some hours a cron will check if you have an image to display. The calendar being located in my kitchen, I run the cron task at mealtimes :-)

Here's what each program stand for:

- **main.py**: The main loop that listens for button events.
- **calendar.py**: displays the Google calendar.
- **meteo.py**: displays weather forecasts from Open Weather.
- **config.py**: configuration of programs. It's in this file that you need to set the Google Calendar calendars, the Open Weather API key, your city for the weather forecast, etc ...

- **clockAllume.py**: Displays current time on the LED strip. The luminoisity of the LEDs is updated according to the time (very bright in the day and more discreet in the night, we will not make a lighthouse either :-)
- **clockEteind.py**: turns off the LED strip.
- **photos.py**: Display an image on a given date. Very handy to display a person's hpicture when this is/her is birthday.
- **bandeauHaut.py**: This short program allows to display a common part to all the different screens. We find the date, the day, the month, the current weather, the outside temperature, the weather forecast for the coming days, etc ...
- **test-XXXXXXX.py**: Allows you to test if your API's are ok.
- **tachesCron.txt: text file for crontasks sample.
