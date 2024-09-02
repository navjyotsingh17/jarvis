import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import pywhatkit as kit
import os
import subprocess
from datetime import datetime
import pyjokes

news_api_key="ff47108b1a1b43b4949c388675928563"

recognizer =sr.Recognizer()
ttsx = pyttsx3.init()

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key = "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")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful virtual assistant named jarvis and your work is give human like response to rach every question that is asked to you."},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    speak(completion.choices[0].message.content)

def processCommand(command):
    print(f"Command :- {command}")
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open github" in command.lower():
        webbrowser.open("https://github.com")    
    elif "news" in command.lower():
        webbrowser.open("http://localhost:8082/") 
       
        # # Making the GET request
        # response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")

        # # Checking if the request was successful
        # if response.status_code == 200:
        #     # Getting the JSON data from the response
        #     data = response.json()
            
        #     articles = data.get("articles", [])

        #     for article in articles:
        #         speak(article["title"])
        # else:
        #     # print(f"Failed to retrieve data. Status code: {response.status_code}")
        #     speak(f"Failed to retrieve data. Status code: {response.status_code}")

    elif command.lower().startswith("play"):
        song = command.lower().split()[1]
        # link = musicLibrary.music[song]
        # webbrowser.open(link)
        print(f"Searching for {song} on YouTube...")
    
        # This will open YouTube in the default browser and play the first video found
        kit.playonyt(song)

    elif command.lower().startswith("open"):
        app_name = command.lower().split()[1]
        print(f"Opening {app_name} on your pc") 
        # subprocess.Popen("C://Users//Lenovo//AppData//Roaming//Zoom//bin//Zoom.exe")
        subprocess.Popen(app_name)

    elif "what's the time" in command:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "joke" in command:
        joke = pyjokes.get_joke() 
        speak(joke)
         
    else:
        aiProcess(command)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=5)
            word =  r.recognize_google(audio,language='en-in')
            
            if(word.lower() == "jarvis"):
                speak("Yes sir.")
                print("Jarvis activated")

            # Listen for command
            with sr.Microphone() as source:
                print("Listening for command...")
                audio = r.listen(source,timeout=2,phrase_time_limit=5)

            command =  r.recognize_google(audio,language='en-in')

            processCommand(command)


        except Exception as e:
            print("Error :- {0}".format(e))
