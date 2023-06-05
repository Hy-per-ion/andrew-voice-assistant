# diksha
import datetime
import os
import signal
import speech_recognition as sr
import pyttsx3
import webbrowser
import re
import pywhatkit
import pyjokes
import requests
import json
import cv2

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 200)


def load_commands(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data["commands"]


commands = load_commands("app/commands.json")


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


def terminate():
    os.kill(os.getpid(), signal.SIGTERM)


# amar

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Andrew. How may I assist you")


def get_time(que):
    if "what is the time" in que:
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


def search_web(que):
    url = "https://www.google.com/search?q=" + que.replace(" ", "+")
    webbrowser.open(url)


def open_web(que):
    url = "https://www." + que.replace(" ", "") + ".com/"
    webbrowser.open(url)


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


def play_song(que):
    speak("Playing " + que + " on YouTube.")
    pywhatkit.playonyt(que)


# prathit

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


def note():
    speak("What do you want to write on your note?")
    notes = recognize_speech()
    speak("Choose a file name!")
    filename = recognize_speech()
    with open(f"{filename}.txt", 'w') as f:
        f.write(notes)
    speak(f"I created the note {filename}")


def take_pic():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    filename = "memories.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    speak(f"Picture taken and saved as {filename}")


def send_whatsapp_message(number, message, hour, minute, wait_time=8, print_wait=True, wait_in_seconds=2):
    pywhatkit.sendwhatmsg(number, message, hour, minute, wait_time, print_wait, wait_in_seconds)
    speak("WhatsApp message sent.")


# kaushik
def handle_query(que):
    matched_command = matching_command(que)
    if matched_command:
        if matched_command == "greeting":
            speak(commands[matched_command]["response"])
        elif matched_command == "name":
            speak("My name is Andrew, I am your virtual assistant")
        elif matched_command == "identity":
            speak("I am your virtual assistant, you can call me Andrew")
        elif matched_command == "time":
            get_time(que)
        elif matched_command == "date":
            get_date()
        elif matched_command == "open_whatsapp":
            webbrowser.open("https://web.whatsapp.com/")
            speak("Opening WhatsApp")
        elif matched_command == "open_youtube":
            webbrowser.open("https://www.youtube.com/")
            speak("Opening YouTube")
        elif matched_command == "open_netflix":
            webbrowser.open('https://www.netflix.com/')
            speak("Opening Netflix")
        elif matched_command == "open_google":
            webbrowser.open('https://www.google.com/')
            speak("Opening Google")
        elif matched_command == "open":
            que = que.replace("open", "")
            open_web(que)
        elif matched_command == "open_github":
            webbrowser.open("https://github.com/Hy-per-ion/andrew-voice-assistant.git")
            speak("Opening GitHub")
        elif matched_command == "weather":
            match = re.search('what is the weather in (.+)', que)
            if match:
                city = match.group(1)
                message = get_weather(city)
                speak(message)
            else:
                speak("What city would you like to know the weather for?")
        elif matched_command == "search":
            que = que.replace("search for", "")
            search_web(que)
        elif matched_command == "play":
            match = re.search('play (.+)', que)
            if match:
                que = match.group(1)
                play_song(que)
            else:
                speak("What song would you like me to play on YouTube?")
        elif matched_command == "joke":
            tell_joke()
        elif matched_command == "note":
            note()
        elif matched_command == "take_pic":
            take_pic()
        elif matched_command == "send_message":
            speak("Please provide the recipient's phone number.")
            number = input("Enter the phone number with the country code: ")
            speak("What message would you like to send?")
            message = recognize_speech()
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute + 1
            send_whatsapp_message(number, message, hour, minute)
        elif matched_command == "conversation":
            speak("what's your favorite color?")
            user_color = recognize_speech()
            if "stop" in user_color.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"Oh, {user_color} is a nice color!")
            speak("Do you have any hobbies?")
            user_hobbies = recognize_speech()
            if "stop" in user_hobbies.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"Oh, that's interesting. I also enjoy {user_hobbies}!")
            speak("What's your favorite movie?")
            user_movie = recognize_speech()
            if "stop" in user_movie.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"Great choice! I've heard good things about {user_movie}.")
            speak("What is your favorite food?")
            user_food = recognize_speech()
            if "stop" in user_food.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"Oh, I love {user_food} too!")
            speak("What is your favorite book?")
            user_book = recognize_speech()
            if "stop" in user_book.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"I've heard great things about {user_book}. It's on my reading list!")
            speak("Do you prefer e-books or physical books?")
            user_preference = recognize_speech()
            if "stop" in user_preference.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"I enjoy {user_preference} too. There's something special about holding a physical book.")
            speak("Tell me about your favorite hobby.")
            user_hobby = recognize_speech()
            if "stop" in user_hobby.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"{user_hobby} sounds like a wonderful hobby!")
            speak("Tell me about your favorite movie.")
            user_movie = recognize_speech()
            if "stop" in user_movie.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"{user_movie} is a classic. I enjoy watching it too!")
            speak("What is your favorite genre of music?")
            user_genre = recognize_speech()
            if "stop" in user_genre.lower():
                speak("Alright, let's end the conversation here.")
                return
            speak(f"I love listening to {user_genre} music. It's so uplifting!")
            speak("It was nice chatting with you!")
        elif matched_command == "terminate":
            speak("Goodbye!")
            exit()
    else:
        speak("I'm sorry, can you repeat that")


def matching_command(user_input):
    for command_name, command_data in commands.items():
        command_variations = command_data["variations"]
        for variation in command_variations:
            if variation in user_input:
                return command_name
    return None


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
