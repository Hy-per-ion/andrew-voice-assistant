# Andrew Voice Assistant

Andrew Voice Assistant is a Python program that uses speech recognition and text-to-speech technology to provide various functionalities and assist users with their daily tasks. The assistant can perform tasks such as telling the time, searching the web, playing music on YouTube, providing weather information, taking notes, and more.

##Features

-Greeting: The assistant greets the user based on the time of the day.
-Time and Date: The assistant can tell the current time and date.
-Web Search: Users can ask the assistant to search the web for any query.
-Open Websites: The assistant can open popular websites like Google, YouTube, Netflix, and more.
-Open Specific Website: Users can ask the assistant to open any specific website by stating the website name.
-Play Music: The assistant can play any song on YouTube based on the user's request.
-Tell Jokes: Users can ask the assistant to tell a joke.
-Weather Information: The assistant can provide weather information for a specific city.
-Take Notes: Users can ask the assistant to take notes and save them with a chosen file name.
-Take Pictures: The assistant can take pictures using the computer's webcam and save them.
-Send WhatsApp Messages: Users can ask the assistant to send WhatsApp messages to a specified phone number.
-Translate Text: Users can ask the assistant to translate text from a specified language to English.
-Conversational Interaction: The assistant engages in a conversation with the user, asking about their favorite color, hobbies, movies, books, and more.
-Termination: Users can ask the assistant to terminate the program.

##Prerequisites
###The following libraries need to be installed to run the program:

-speech_recognition
-pyttsx3
-webbrowser
-re
-pywhatkit
-pyjokes
-requests
-json
-cv2
-googletrans

##Install the required libraries using the following command:
```bash
Copy code
pip install speechrecognition pyttsx3 pywhatkit pyjokes requests opencv-python googletrans
```
Usage

##Run the Python file using the following command:
```bash
Copy code
python run.py
```
The assistant will greet you and wait for your command.

Speak your command or question clearly into the microphone.

The assistant will process your command and provide a response or perform the requested action.

Continue interacting with the assistant by speaking your commands or questions.

##Customization
The assistant's functionalities and responses can be customized by modifying the commands.json file. The file contains a list of commands and their variations, along with corresponding responses. You can add, remove, or modify commands as per your requirements.

To customize the assistant's responses, you can modify the handle_query function in the code. This function maps user commands to specific actions or responses.
