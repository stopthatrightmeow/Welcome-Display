from __future__ import print_function
from flask import Flask, render_template
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dateutil import parser
from bs4 import BeautifulSoup
import random
import feedparser
import requests
import time
import os.path

app = Flask(__name__)

@app.route("/")
def index():
    date = datetime.now().strftime('%A, %B %d')

    other_date = datetime.today()
    # News Article
    try:
        rss_num = random.randint(1, 25)
        rss_feed_parse = feedparser.parse('https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en')
        news_article = rss_feed_parse['entries'][rss_num]['title']
    except:
        news_article = 'No Internet'

    # Background
    if other_date.strftime('%m') == '10': # Halloween
        image = os.listdir("static/Backgrounds/halloween/")
        if '.DS_Store' in image:
            image.remove('.DS_Store')
        selected_image = random.choice(image)
        file_path = 'Backgrounds/halloween/'
    elif other_date.strftime('%m') == '12': # Christmas
        image = os.listdir("static/Backgrounds/christmas/")
        if '.DS_Store' in image:
            image.remove('.DS_Store')
        selected_image = random.choice(image)
        file_path = 'Backgrounds/christmas/'
    elif other_date.strftime('%m, %d') == '01, 01': # Birthday
        image = os.listdir("static/Backgrounds/birthday/")
        if '.DS_Store' in image:
            image.remove('.DS_Store')
        selected_image = random.choice(image)
        file_path = 'Backgrounds/birthday/'
    elif other_date.strftime('%m, %d') == '07, 04': # Independence Day
        image = os.listdir("static/Backgrounds/america/")
        if '.DS_Store' in image:
            image.remove('.DS_Store')
        selected_image = random.choice(image)
        file_path = 'Backgrounds/america/'
    else:
        image = os.listdir("static/Backgrounds/normal/")
        if '.DS_Store' in image:
            image.remove('.DS_Store')
        selected_image = random.choice(image)
        file_path='Backgrounds/normal/'
    
    background = file_path + selected_image
    print(background)


    # Countdown
    msg_list = ['Day 3,532 of Quarentine: "I can\'t be with people, and I can\'t be alone."', 'Hey I love your face',
                'Your face, I like that shit.', "You're perfect", "Where's Waldo, social disting edition", 
                "You smell good, is that Purell you're wearing?...", "Social distancing champion: Big foot",
                "The police want to remind you that running from them is not social distancing.", 
                "The only thing that seperates us from the animals is our ability to accessorize.", "You should get some sushi today :)",
                "A day without sunshine is like, you know, night.", "Accept who you are. Unless you're a serial killer...",
                "Hey, you, yes you, I LOVE YOU!", "When life gives you lemons, add them to your tequila.",
                "Life, it's not rocket surgery.", "Sometimes life goes over like a pregnant pole vaulter..."]
                
    if other_date.strftime('%m') == '10' and other_date.strftime('%d') == '31':
        message = "Happy Halloween ghouls and ghosts, it's time to trick or treat!"
    elif other_date.strftime('%m') == '10' and int(other_date.strftime('%d')) < 31:
        days_left = 31 - int(other_date.strftime('%d'))
        message = "{} days until Halloween!".format(days_left)
    elif other_date.strftime('%m') == '12' and int(other_date.strftime('%d')) < 26:
        if other_date.strftime('%d') == '24':
            message = "Santa's is on his way, Merry Christmas eve!"
        elif other_date.strftime('%d') == '25':
            message = "Merry Christmas!"
        else:
            days_left = 25 - int(other_date.strftime('%d'))
            message = '{} days left until Christmas!'.format(days_left)
    elif other_date.strftime('%m, %d') == '01, 01':
        message = 'Happy New Year!'
    elif other_date.strftime('%m, %d') == '07, 04':
        message = 'Happy Independence day! F*ck yeah America!'
    elif other_date.strftime('%m, %d') == '01, 01':
        message = 'Happy birthday!'
    else:
        message = random.choice(msg_list)

    # Weather
    # URLs, API's, and City ID (to be changed when needed)
    try:
        baseUrl = 'http://api.openweathermap.org/data/2.5/weather?'
        apiKey = "INSERT YOUR API KEY HERE"
        zip = 'ENTER YOUR ZIP CODE HERE'
        finalUrl = baseUrl + 'zip=' + zip + '&APPID=' + apiKey + '&units=imperial'
        weatherData = requests.get(finalUrl).json()

        weatherDict = {
            'thunderstorms': [200, 201, 202, 210, 211, 212, 221, 230, 231, 232],
            'clouds': [801, 802, 803, 804],
            'drizzle': [300, 301, 302, 310, 311, 312, 313, 314, 321],
            'rain': [500, 501, 502, 503, 504, 511, 520, 521, 522, 531],
            'snow': [600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622],
            'atmosphere': [701, 711, 721, 731, 741, 751, 761, 762, 771],
            'tornado': [781],
            'clear': [800]
        }

        if weatherData['weather'][0]['id'] in weatherDict['thunderstorms']:
            weather_pic = 'WeatherIcons/thunderstorm.png'
            description = 'Thunderstorms'
        elif weatherData['weather'][0]['id'] in weatherDict['clouds']:
            if time.localtime().tm_hour < 6 or time.localtime().tm_hour > 18:
                weather_pic = 'WeatherIcons/nightClouds.png'
                description = 'Cloudy Skies'
            else:
                weather_pic = 'WeatherIcons/cloudy.png'
                description = 'Cloudy Skies'
        elif weatherData['weather'][0]['id'] in weatherDict['drizzle']:
            weather_pic = 'WeatherIcons/drizzle.png'
            description = 'Drizzly Skies'
        elif weatherData['weather'][0]['id'] in weatherDict['rain']:
            weather_pic = 'WeatherIcons/rain.png'
            description = 'RainySkies'
        elif weatherData['weather'][0]['id'] in weatherDict['snow']:
            weather_pic = 'WeatherIcons/snow.png'
            description = 'Snowy Skies'
        elif weatherData['weather'][0]['id'] in weatherDict['atmosphere']:
            weather_pic = 'WeatherIcons/smog.png'
            description = 'Hazy Skies'
        elif weatherData['weather'][0]['id'] in weatherDict['tornado']:
            weather_pic = 'WeatherIcons/tornado.png'
            description = 'Uh, Tornado...'
        elif weatherData['weather'][0]['id'] in weatherDict['clear']:
            if time.localtime().tm_hour < 6 or time.localtime().tm_hour > 18:
                weather_pic = 'WeatherIcons/nightClear.png'
                description = 'Clear Skies'
            else:
                weather_pic = 'WeatherIcons/clear.png'
                description = 'Clear Skies'
    except:
        weather_pic = 'WeatherIcons/clear.png'
        description = '??????????'

    try:
        temperature = str(round(weatherData['main']['temp'])) + "°F"
        highlow = str(round(weatherData['main']['temp_max'])) + '/' + \
            str(round(weatherData['main']['temp_min'])) + ' | ' + \
            str(round(weatherData['main']['humidity'])) + '%'
    except:
        temperature = "??°F"
        highlow = "??/?? | ???%"


    # Google Calendar
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        calEvents = {}
        calEvents['work'] = []
        calEvents['normalEvent'] = []

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime')
            try:
                # Correcting the start time
                newStartTime = str(int(start[11:13]) + 2)
                newEndTime = str(int(end[11:13]) + 2)
            except ValueError:
                newEndTime = "All day event"

            try:
                if newEndTime == 'All day event':
                    calendarItem = newEndTime + ' - ' + event['summary']
                else:
                    startDate = parser.parse(start).strftime("%A %B %d at {}:%M until ".format(newStartTime))
                    endDate = parser.parse(end).strftime("{}:%M".format(newEndTime))
                    calendarItem = startDate + endDate + ' - ' + event['summary']

                if event['summary'].lower() == 'work':
                    calEvents['work'].append(calendarItem)
                else:
                    calEvents['normalEvent'].append(calendarItem)

            except:
                calEvents['normalEvent'].append(' ')
                calEvents['normalEvent'].append(' ')
                calEvents['normalEvent'].append(' ')

    except:
        calEvents = {}
        calEvents['work'] = []
        calEvents['normalEvent'] = []

        calEvents['normalEvent'].append(' ')
        calEvents['normalEvent'].append(' ')
        calEvents['normalEvent'].append(' ')

    if len(calEvents['normalEvent']) == 0:
        cal_header = 'There are no upcoming events.'
        cal_one = " "
        cal_two = " "
        cal_three = " "
    elif len(calEvents['normalEvent']) == 1:
        cal_header = 'Upcoming Events'
        cal_one = calEvents['normalEvent'][0]
        cal_two = " "
        cal_three = " "
    elif len(calEvents['normalEvent']) == 2:
        cal_header = 'Upcoming Events'
        cal_one = calEvents['normalEvent'][0]
        cal_two = calEvents['normalEvent'][1]
        cal_three = " "
    elif len(calEvents['normalEvent']) >= 3:
        cal_header = 'Upcoming Events'
        cal_one = calEvents['normalEvent'][0]
        cal_two = calEvents['normalEvent'][1]
        cal_three = calEvents['normalEvent'][2]

    #Pihole Ads
    try:
        response = requests.get("http://pi.hole/admin/api.php?summary")
        data = response.json()
        ads_blocked = data['ads_blocked_today']
        total_queries = data['dns_queries_today']
        ads = f'{ads_blocked} ads blocked out of {total_queries} total queries.'
    except:
        ads = 'No Internet'

    return render_template('index.html', cal_header=cal_header, cal_one=cal_one, cal_two=cal_two,
                           cal_three=cal_three, date=date, background=background, rss=news_article,
                           countdown=message, weather_pic=weather_pic, temperature=temperature, highlow=highlow,
                           description=description, ads=ads)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
