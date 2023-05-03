import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import vlc
import re
import pywhatkit
import pyjokes
import requests
import json

r = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that"
        except sr.RequestError:
            return "Sorry, I am not able to process your request"


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Andrew . How may i assist you")


def get_time(query):
    if "what is the time" in query:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        if hour == 0:
            hour = 12
            time = "AM"
        elif hour < 12:
            time = "AM"
        elif hour == 12:
            time = "PM"
        else:
            hour -= 12
            time = "PM"
        time_string = f"{hour}:{minute:02d} {time}"
        speak(f"The time is {time_string}.")


def get_date():
    today = datetime.date.today()
    date_string = today.strftime("%B %d, %Y")
    engine.say(f"Today's date is {date_string}")
    engine.runAndWait()


def get_weather(city):
    api_key = "f3ab91ce4b4309f3a6a17172fa7c3928"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] != "404":
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        message = f"The weather in {city} is {weather}, with a temperature of {temperature} degrees Celsius, feels like {feels_like} degrees Celsius, humidity of {humidity} percent, and a wind speed of {wind_speed} meters per second."
        return message
    else:
        return "Sorry, I could not find the weather information for that city."


def search_web(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)


def play_song(query):
    speak("Playing " + query + " on YouTube.")
    pywhatkit.playonyt(query)


player = vlc.MediaPlayer()


def play_music():
    global player
    music_path = "app/topg.mp3"
    media = vlc.Media(music_path)
    player.set_media(media)
    player.play()


def stop_music():
    global player
    player.stop()


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


def handle_query(query):
    if "what is the time" in query:
        get_time(query)
    elif "what is the date" in query:
        get_date()
    elif "what is your name" in query:
        speak("My name is andrew, I am your virtual assistant") 
    elif "who are you" in query:
        speak("I am your virtual assistant, you can call me andrew")
    elif "open whatsapp" in query:
        webbrowser.open("https://web.whatsapp.com/")
        speak("Opening WhatsApp")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube")
    elif "open netflix" in query:
        webbrowser.open('https://www.netflix.com/')
        speak("Opening netflix")
    elif "open google" in query:
        webbrowser.open('https://www.google.com/')
        speak("Opening google")
    elif "open github" in query:
        webbrowser.open("https://github.com/Hy-per-ion/andrew-voice-assistant.git")
        speak("Opening github")
    elif "what is the weather in" in query:
        match = re.search('what is the weather in (.+)', query)
        if match:
            city = match.group(1)
            message = get_weather(city)
            speak(message)
        else:
            speak("What city would you like to know the weather for?")
    elif "search for" in query:
        query = query.replace("search for", "")
        search_web(query)
    elif "play" in query:
        match = re.search('play (.+)', query)
        if match:
            query = match.group(1)
            play_song(query)
        else:
            speak("What song would you like me to play on YouTube?")
    elif "play music" in query:
        play_music()
    elif "stop music" in query:
        stop_music()
    elif "tell me a joke" in query:
        tell_joke()
    elif "terminate" in query:
        speak("Goodbyee!")
        exit()
    else:
        speak("I'm sorry, can you repeat that")


def welcome():
    global already_welcomed
    if not already_welcomed:
        wishMe()
        already_welcomed = True


already_welcomed = False

while True:
    welcome()
    query = recognize_speech().lower()
    handle_query(query)
