from Jarvis import JarvisAssistant
import re
import os
import random
import pprint
import datetime
import requests
import sys
import urllib.parse  
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from PIL import Image
from threading import Thread
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config
import speech_recognition as sr

obj = JarvisAssistant()

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'niteesh2june@gmail.com',
    'my official email': 'niteesh2june@gmail.com',
    'my second email': 'niteesh2june@gmail.com',
    'my official mail': 'niteesh2june@gmail.com',
    'my second mail': 'niteesh2june@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

def speak(text):
    obj.tts(text)

app_id = config.wolframalpha_id

def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None

def startup():
    # speak("Initializing Jarvis")
    speak("Setting up my artificial intelligence")
    speak("Checking the internet connection")
    # speak("Wait a moment sir")
    speak("Loading all the details from Stark industry databases")
    speak("All systems have been activated")
    # speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. I'm online. How can i help you")

class VoiceCommandListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.stop_listening = None
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 300

    def start_listening(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.stop_listening = self.recognizer.listen_in_background(self.mic, self.callback)

    def callback(self, recognizer, audio):
        try:
            command = recognizer.recognize_google(audio).lower()
            print("Recognized:", command)
            self.process_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Speech Recognition API unavailable")

    def stop(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)

    def process_command(self, command):
        if re.search('date', command):
            date = obj.tell_me_date()
            speak(date)

        elif "time" in command:
            time_c = obj.tell_time()
            speak(f"Sir the time is {time_c}")

        elif re.search('launch', command):
            dict_app = {'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'}
            app = command.split(' ', 1)[1]
            path = dict_app.get(app)
            if path:
                speak('Launching: ' + app)
                obj.launch_any_app(path_of_app=path)
            else:
                speak('Application path not found')

        elif command in GREETINGS:
            speak(random.choice(GREETINGS_RES))

        elif re.search('open', command):
            domain = command.split(' ')[-1]
            obj.website_opener(domain)
            speak(f'Opening {domain}')

        elif re.search('weather', command):
            city = command.split(' ')[-1]
            weather_res = obj.weather(city=city)
            speak(weather_res)

        elif re.search('tell me about', command):
            topic = command.split(' ')[-1]
            wiki_res = obj.tell_me(topic)
            speak(wiki_res)

        elif "buzzing" in command or "news" in command:
            news_res = obj.news()
            speak('Todays Headlines:')
            for index, article in enumerate(news_res[:3]):
                speak(article['title'])

        elif 'search google for' in command:
            obj.search_anything_google(command)

        elif "play music" in command:
            music_dir = "F://Songs//Imagine_Dragons"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'youtube' in command:
            video = command.split(' ')[1]
            pywhatkit.playonyt(video)

        elif "email" in command:
            sender_email = config.email
            sender_password = config.email_password
            speak("Whom do you want to email?")
            recipient = obj.mic_input()
            receiver_email = EMAIL_DIC.get(recipient)
            if receiver_email:
                speak("Subject?")
                subject = obj.mic_input()
                speak("Message?")
                message = obj.mic_input()
                msg = f'Subject: {subject}\n\n{message}'
                obj.send_mail(sender_email, sender_password, receiver_email, msg)
                speak("Email sent successfully")
            else:
                speak("Email not found")

        elif "calculate" in command or "what is" in command or "who is" in command:
            answer = computational_intelligence(command)
            speak(answer)

        elif "what do i have" in command or "do i have plans" in command:
            obj.google_calendar_events(command)

        elif "make a note" in command:
            speak("What should I note?")
            note_text = obj.mic_input()
            obj.take_note(note_text)

        elif "close the note" in command:
            os.system("taskkill /f /im notepad++.exe")

        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "system" in command:
            sys_info = obj.system_info()
            speak(sys_info)

        elif "where is" in command:
            place = command.split('where is ', 1)[1]
            current_loc, target_loc, distance = obj.location(place)
            city = target_loc.get('city', '')
            state = target_loc.get('state', '')
            country = target_loc.get('country', '')
            if city:
                res = f"{place} is in {state}, {country}. {distance} km away."
            else:
                res = f"{state} is in {country}. {distance} km away."
            speak(res)

        elif "ip address" in command:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "switch window" in command:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "current location" in command:
            city, state, country = obj.my_location()
            speak(f"You are in {city}, {state}, {country}")

        elif "take screenshot" in command:
            speak("By what name?")
            name = obj.mic_input()
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot taken")

        elif "show me the screenshot" in command:
            try:
                img = Image.open(f"{name}.png")
                img.show()
            except:
                speak("Couldn't find the screenshot")

        elif "hide all files" in command:
            os.system("attrib +h /s /d")
            speak("Files hidden")

        elif "make files visible" in command:
            os.system("attrib -h /s /d")
            speak("Files visible")

        elif "goodbye" in command or "offline" in command:
            speak("Going offline")
            self.stop()
            sys.exit()

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        startup()
        self.listener = VoiceCommandListener()
        self.listener.start_listening()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.startExecution = MainThread()
        self.startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.ui.textBrowser.setText(current_date.toString(Qt.ISODate))
        self.ui.textBrowser_2.setText(current_time.toString('hh:mm:ss'))

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())