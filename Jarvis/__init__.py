import speech_recognition as sr
import pyttsx3

from Jarvis.features import date_time
from Jarvis.features import launch_app
from Jarvis.features import website_open
from Jarvis.features import weather
from Jarvis.features import wikipedia
from Jarvis.features import news
from Jarvis.features import send_email
from Jarvis.features import google_search
from Jarvis.features import google_calendar
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Use Microsoft George (male voice)
for voice in voices:
    if "george" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 175)  # Adjust speed if needed

class JarvisAssistant:
    def __init__(self):
        pass

    def mic_input(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
            except:
                print('Please try again')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False

    def tts(self, text):
        try:
            engine.say(text)
            engine.runAndWait()
            return True
        except:
            print("Sorry I couldn't handle this input")
            return False

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, path_of_app):
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        return website_open.website_opener(domain)

    def weather(self, city):
        try:
            return weather.fetch_weather(city)
        except Exception as e:
            print(e)
            return False

    def tell_me(self, topic):
        return wikipedia.tell_me_about(topic)

    def news(self):
        return news.get_news()
    
    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)
        if date:
            return google_calendar.get_events(date, service)

    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)

    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        return loc.my_location()
