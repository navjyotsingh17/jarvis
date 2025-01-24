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
from dotenv import load_dotenv
import sys
from typing import Dict, Union
import winreg  # Windows only

recognizer =sr.Recognizer()
ttsx = pyttsx3.init()

load_dotenv()

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key = os.getenv("OPEN_AI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful virtual assistant named jarvis and your work is give human like response to rach every question that is asked to you. You can also perform some basic tasks like opening websites or applications, playing music, telling jokes, accessing news, data over the web, etc."},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    speak(completion.choices[0].message.content)

def get_installed_apps() -> Dict[str, Dict[str, Union[str, None]]]:
    """Dynamically find installed applications based on the operating system"""
    apps = {'windows': {}, 'linux': {}, 'darwin': {}}
    
    if sys.platform == 'win32':
        # Windows registry lookup for installed applications
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths") as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    app_name = winreg.EnumKey(key, i)
                    try:
                        with winreg.OpenKey(key, app_name) as appkey:
                            path = winreg.QueryValue(appkey, None)
                            apps['windows'][app_name.lower().replace('.exe', '')] = path
                    except:
                        continue
        except:
            pass

        # Add common Windows apps not in registry
        common_apps = {
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe'
        }
        apps['windows'].update(common_apps)

    return apps

# Initialize APP_PATHS dynamically
APP_PATHS = get_installed_apps()

def find_application(app_name: str) -> Union[str, None]:
    """Find an application across all possible locations"""
    platform = sys.platform
    os_type = 'windows' if platform == 'win32' else 'linux' if platform.startswith('linux') else 'darwin'
    
    # Check known applications first
    if app_name.lower() in APP_PATHS[os_type]:
        return APP_PATHS[os_type][app_name.lower()]
    
    # Fallback: Search in system PATH
    try:
        if os_type == 'windows':
            which_cmd = f'where {app_name}'
        else:
            which_cmd = f'which {app_name}'
            
        result = subprocess.check_output(which_cmd, shell=True, stderr=subprocess.DEVNULL)
        return result.decode().strip().split('\n')[0]
    except:
        return None

def open_application(app_name: str):
    """Open an application using system-appropriate method"""
    platform = sys.platform
    app_path = find_application(app_name)
    
    if not app_path:
        print(f"❌ Application {app_name} not found")
        return

    try:
        if platform == 'win32':
            os.startfile(app_path) if app_path.endswith('.exe') else subprocess.Popen(app_path)
        elif platform == 'darwin':
            subprocess.run(['open', app_path], check=True)
        else:
            subprocess.run([app_path], check=True)
        print(f"✅ Opened {app_name}")
    except Exception as e:
        print(f"❌ Error opening {app_name}: {str(e)}")

# Rest of your existing code...

def processCommand(command):
    print(f"Command :- {command}")
    if "search" in command:
        search_query = command.split("search")[1]
        webbrowser.open(f"https://google.com/search?q={search_query}")
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

    elif "play" in command:
        song = command.lower().split()[1]
        # link = musicLibrary.music[song]
        # webbrowser.open(link)
        print(f"Searching for {song} on YouTube...")
    
        # This will open YouTube in the default browser and play the first video found
        kit.playonyt(song)

    elif "open" in command:
        app_name = command.lower().split()[1]
        print(f"Opening {app_name} on your pc") 
        # subprocess.Popen("C://Users//Lenovo//AppData//Roaming//Zoom//bin//Zoom.exe")
        open_application(app_name)

    elif "what's the time" in command:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "joke" in command:
        joke = pyjokes.get_joke() 
        speak(joke)
    
    elif "exit" in command:
        speak("Goodbye sir. Have a nice day.")
        exit()
         
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
