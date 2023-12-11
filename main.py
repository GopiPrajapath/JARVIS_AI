import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import argparse
from enum import Enum
import logging
import openai

logging.basicConfig(level=logging.INFO)

openai.api_key = 'OPEN AI API KEY'


class Commands(Enum):
    TIME = 1
    DATE = 2
    OPEN = 3
    WIKIPEDIA = 4
    WEATHER = 5
    QUIT = 6


responses = {}


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
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
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {current_time}")


def get_date():
    today = datetime.date.today()
    speak(f"Today is {today}")


def open_app(app):
    os.system(f"start {app}")


def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak(f"According to Wikipedia, {results}")


def get_weather(city):
    # API call to weather API
    speak(f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius")


def ask_question(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    speak(response)

    if response:
        # Save the answer to a file
        with open("output.txt", "a") as file:
            file.write(f"Question: {question}\n")
            file.write(f"Answer: {response}\n\n")

        return response
    else:
        return "Sorry, I couldn't find an answer."
def process_text_query(query):
    try:
        if 'what is time' in query:
            get_time()

        elif 'what is date' in query:
            get_date()

        elif Commands.OPEN.name in query:
            app = query.replace('open', '').strip()
            open_app(app)

        elif Commands.WIKIPEDIA.name in query:
            question = query.replace(Commands.WIKIPEDIA.name, '')
            search_wikipedia(question)

        elif Commands.WEATHER.name in query:
            city = query.replace(Commands.WEATHER.name, '').strip()
            get_weather(city)

        elif 'exit' in query:
            speak("Goodbye! Have a nice day.")
            exit()

        else:
            speak("I don't have an answer for that. Let me query my AI.")
            ask_question(query)


    except Exception as e:
        print(e)
        speak("Sorry, I am unable to perform this action at the moment.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Virtual Assistant")
    parser.add_argument('--query', type=str, default=None, help='Query to process')
    args = parser.parse_args()

    print("Initializing virtual assistant...")
    speak("Hi, I am Jarvis, your virtual assistant. How may I assist you?")

    while True:
        if args.query:
            process_text_query(args.query)
        else:
            query = get_audio().lower()
            if query != 'none':
                process_text_query(query)

