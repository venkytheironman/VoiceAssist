import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import urllib.request
import smtplib
import json
from PyDictionary import PyDictionary
import requests
import pyjokes
import os
import pywhatkit as kit
from requests import get
import pyautogui
import wolframalpha

#selecting voice and setting speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#converts text to speech

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)
#greets user

# Greeting the user
def greetUser():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
       
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
         
    else:
        speak("Good Evening!")
       
    asstname = str("Samantha")
    speak("I am your assistant, " + asstname)
    speak("Please tell me how can I help you?")
   
#It takes input from the user with the help of microphone and returns string/text output

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")  
        query = r.recognize_google(audio, language='en-IN')
        query = query.lower()
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        speak("say that again please...")
        return "None"
    return query

#Sends email

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('samantha.voiceasst@gmail.com', 'Miniproject2021')
    server.sendmail('samantha.voiceasst@gmail.com', to, content)
    server.close()

#Finds meaning of word

def Find_meaning(word):
    dictionary=PyDictionary()
    mean={}
    mean=dictionary.meaning(word)
    speak("Alright here is the information you asked for")
    for key in mean.keys():
        speak("when "+str(word)+" is used as a "+str(key)+" then the meanings are")
        for val in mean[key]:
                    speak(val)
        print()

if __name__ == "__main__":
    greetUser()
    while True:
    #if 1:
    #storing user input in query
        query = take_command().lower()

    #Logic for executing tasks based on query

        #opens wikipedia
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        #To open youtube    
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            speak("Opening youtube")

        elif 'song on youtube' in query:
            song = query.replace('play', '')
            speak('playing '+ song)
            kit.playonyt(song) 

        #opens google
        elif 'open google' in query:
            speak("What should I search on google")
            search= take_command().lower()
            webbrowser.open(search)

        #current location
        elif "current location" in query:
            speak("Getting IP address for finding the location")
            try:
                ipAdd= requests.get("https://api.ipify.org").text
                url = "https://get.geojs.io/v1/ip/geo/"+ipAdd+".json"
                geo_req = requests.get(url)
                geo_data = geo_req.json()
                city = geo_data["city"]
                country = geo_data["country"]
                speak (f"you are currently in {city} city of country {country} ")
               
            except Exception as e:
                speak("Unable tp find your location. please check network connectivity")
                pass

        #shows weather report    
        elif 'weather' in query:
            speak("getting the API key")
            api_key = "ad2e2c0aa1ec8b41a089c9b3e5b0d5c4"
            weather_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak("For which city you want me too find the weather?")
            location = take_command()
            speak("Showing you the weather report")
            url = weather_url + "appid=" + api_key + "&q=" + location 
            js = requests.get(url).json() 
            if js["cod"] != "404":
                weather = js["main"] 
                temp = weather["temp"] 
                hum = weather["humidity"] 
                desc = js["weather"][0]["description"]
                resp_string = " The temperature in Kelvin is " + str(temp) + " The humidity is " + str(hum) + " and The weather description is "+ str(desc)
                speak(resp_string)
            else:
                speak("City Not Found") 
        
        #shows news report
        elif 'news' in query:
            speak("taking you to today's news headlines")
            webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
        
        #plays music
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)   
            os.startfile(os.path.join(music_dir, songs[0]))
        
        #opens notepad
        elif 'notepad' in query:
            dpath="C:\\Windows\\system32\\notepad.exe"
            os.startfile(dpath)
            speak("opening notepad")
            
        #Closes the notepad
        elif "close notepad" in query:
            speak("Closing the notepad")
            os.system("taskkill /f /im notepad.exe")
            
        #To send Message to Whatsapp
        elif "send message" in query or "text" in query:
            speak("What message would you like to send?")
            msg=take_command()
            kit.sendwhatmsg(f"+917741939354",msg,14,13)
            
        # To Switch the window   
        elif "switch window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")

        #tells current time
        elif 'time' in query or "tell me time" in query:
            strTime = datetime.datetime.now().strftime("%H hour:%M minute:%S second")    
            speak(f"The current time is {strTime}")

        #shows today's date
        elif 'date' in query or "tell me the date" in query:
            strDate= datetime.datetime.today().strftime("%Y-%m-%d")
            speak(f"Today's date  is {strDate}")
           
        elif "solve" in query or "calculate" in query or "calculation" in query:
            app = wolframalpha.Client("RP4LH9-549GKW38HK")
            speak("what should I calculate")
            que = take_command().lower()
            res = app.query(que)
            speak("the answer is")
            speak(next(res.results).text)
            
        # To set the Alarm
        elif "set alarm" in query:
            n = int(datetime.datetime.now().hour)
            if n==22:
                music_dir = 'E"\\music'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[0]))
            
        #sends email
        elif 'send email to alexa' in query or "send mail to alexa" in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "apoorva.jodh66@gmail.com"    
                sendEmail(to, content)
                speak("Email has been successfully sent!")
                
            except Exception as e:
                print(e)
                speak("Sorry,I am not able to send this email.Please try again")    
                
        #searches for meaning of given word
        elif "open dictionary" in query or "meaning" in query or "means" in query:
            speak("what word should I look for?")
            userword= take_command()
            Find_meaning(userword)
        
        #tells joke
        elif "tell me joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)

        #normal chats    
        elif 'how are you' in query:
            speak("I am very well, Thanks for asking \nWhat about you?")
 
        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif "thank you" in query or "thanks" in query:
            speak("pleasure is all mine")
            
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
            
        elif "restart the system" in query:
            os.system("restart /r /t 5")
        
        elif "functions" in query or 'what can you do' in query:
            speak("Here is the list of things that I can do for you")
            speak("Access Wikipedia, Browse Google,YouTube,Facebook\nFind current location, Get weather report")
            speak("Get news report, Open or close application\nSend mail or message, Switch window\nTell time and date, Do calculation")
            speak("Set alarm, Find meaning\nTell joke, Restart or shutdown system")
      
        elif 'exit' in query or 'stop listening' in query:
            speak("Thanks for giving me your time\n\n")
            exit()

