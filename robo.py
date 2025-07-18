import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import plyer as pl
from youtubesearchpython import VideosSearch
import psutil
import os

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak out text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user based on time of day
def wishMe(start, name=None):
    hour = int(datetime.datetime.now().hour)
    if start:
        if 0 <= hour < 12:
            speak(f"Good Morning, {name}!")
        elif 12 <= hour < 18:
            speak(f"Good Afternoon, {name}!")
        else:
            speak(f"Good Evening, {name}!")
        speak(f"How can I assist you today, {name}?")
    else:
        speak('Goodbye, sir')
        if 0 <= hour < 12:
            speak("Have a good day!")
        elif 18 <= hour < 24:
            speak("Have a good night!")

# Function to listen to the user's voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

# Function to remind the user to drink water and take breaks
def waterReminder():
    minute = int(datetime.datetime.now().minute)
    if minute == 0 or minute == 30:
        pl.notification.notify(
            title='Break Reminder',
            message='Time to take a break and drink some water!',
            timeout=60
        )
        speak("Sir, it's time to take a break and drink some water.")

# Function to check and notify reminders
def checkReminder(reminders):
    current_hour = int(datetime.datetime.now().hour)
    current_minute = int(datetime.datetime.now().minute)
    for reminder in reminders:
        if current_hour == reminder[0] and current_minute == reminder[1]:
            pl.notification.notify(
                title='Reminder from Robo',
                message=reminder[2],
                timeout=60
            )
            speak(f'Sir, here is a reminder to {reminder[2]}')
            reminders.remove(reminder)

# Function to open specific applications or websites
def openApplication(app_name):
    if app_name == "youtube":
        speak('Opening YouTube.')
        webbrowser.open("https://www.youtube.com")
    elif app_name == "google":
        speak('Opening Google.')
        webbrowser.open("https://www.google.com")
    elif app_name == "whatsapp":
        speak('Opening WhatsApp Web.')
        webbrowser.open("https://web.whatsapp.com")
    elif app_name == "instagram":
        speak('Opening Instagram.')
        webbrowser.open("https://www.instagram.com")
    elif app_name == "file":
        file_path = input("Please specify the file path to open: ")
        if os.path.exists(file_path):
            speak(f"Opening file located at {file_path}")
            os.startfile(file_path)
        else:
            speak("The file path does not exist. Please check and try again.")

# Function to close an application
def closeApplication(app_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == app_name.lower():
            proc.terminate()
            speak(f"{app_name} has been closed.")

# Main task handler
def Tasks(query):
    if 'search in browser' in query:
        query = query.replace('search in browser', '')
        speak(f'Opening search for {query} in the browser.')
        webbrowser.open(f'https://www.google.com/search?q={query}')
    elif 'search in youtube' in query:
        query = query.replace('search in youtube', '')
        speak(f'Searching {query} on YouTube.')
        webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
    elif 'search in wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query:
        openApplication('youtube')
    elif 'open google' in query:
        openApplication('google')
    elif 'open whatsapp' in query:
        openApplication('whatsapp')
    elif 'open instagram' in query:
        openApplication('instagram')
    elif 'open file' in query:
        openApplication('file')
    elif 'close notepad' in query:
        closeApplication('notepad.exe')
    elif 'play in youtube' in query:
        query = query.replace('play in youtube', '')
        speak(f'Playing {query} on YouTube.')
        videosSearch = VideosSearch(query, limit=1)
        url = videosSearch.result()['result'][0]['link']
        webbrowser.open(url)

# Main logic
if __name__ == "__main__":
    reminders = []

    while True:
        query = takeCommand().lower()

        if 'hello' in query:
            speak('Hello sir, I am Robo!')
            speak("What is your name?")
            name = takeCommand()

            wishMe(True, name)

            while True:
                query = takeCommand().lower()

                if 'set reminder' in query or 'set a reminder' in query:
                    speak("What time should I set the reminder for? Please specify in hours and minutes.")
                    reminder_time = takeCommand()
                    speak("What is the reminder about?")
                    reminder_text = takeCommand()
                    time_parts = reminder_time.split()
                    if len(time_parts) == 2:
                        hour, minute = int(time_parts[0]), int(time_parts[1])
                        reminders.append((hour, minute, reminder_text))
                        speak(f"Reminder set for {reminder_time}.")
                    else:
                        speak("Sorry, I didn't understand the time format. Please try again.")

                elif 'introduce yourself' in query:
                    speak(f'Hello {name}! I am Robo, your personal assistant, designed to make your tasks easier.')

                elif 'exit' in query:
                    wishMe(False, name)
                    exit(0)

                Tasks(query)
                waterReminder()
                checkReminder(reminders)

        waterReminder()
        checkReminder(reminders)
