import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import vlc
import re
import pywhatkit
import pyjokes

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
            meridiem = "AM"
        elif hour < 12:
            meridiem = "AM"
        elif hour == 12:
            meridiem = "PM"
        else:
            hour -= 12
            meridiem = "PM"
        time_string = f"{hour}:{minute:02d} {meridiem}"
        speak(f"The time is {time_string}.")

def get_date():
    today = datetime.date.today()
    date_string = today.strftime("%B %d, %Y")
    engine.say(f"Today's date is {date_string}")
    engine.runAndWait()
    
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
    elif "andrew mode" in query:
        speak("what colour is your bugatti")
    elif "terminate" in query:
        speak("Goodbye!")
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
