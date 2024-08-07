import pyttsx3 
import spacy
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import pyjokes
import smtplib
from googletrans import Translator
from gtts import gTTS
import translate
import random


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


nlp = spacy.load('en_core_web_sm')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        r.energy_threshold = 4000
    
        audio = r.listen(source)
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except sr.WaitTimeoutError:
        print("Timeout exceeded. No speech detected.")
        return "None"

    except Exception as e:
        print(f"Recognition error: {e}")
        print("Say that again please...")
        return "None"    

    # except Exception as e:
    #     # print(e)    
    #     print("Say that again please...")  
    #     return "None"
    

    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('kunalkumarnawada97087@gmail.com', 'atja raor jclw ddej')
    server.sendmail('kunalkumarnawada97087@gmail.com', to, content)
    server.close()

def tellJoke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def translateText(text, target_language):
    try:
        translator = Translator()
        translated = translator.translate(text, src='auto', dest=target_language)
        translated_text = translated.text
        return translated_text
    except Exception as e:
        print(e)
        return "Sorry, I couldn't perform the translation."

news_api_key = 'b2459962112b425e9e4aff35b1985045'
weather_api_key = '6e99dcb4e1d0d86471499f0c66beae8a'


import requests

def get_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    articles = news_data['articles']

    articles = articles[:2]
    
    for article in articles:
        title = article['title']
        description = article['description']
        
        print(title)
        speak(title)
        #speak(description)
        

import requests

def get_weather(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data['cod'] == 200:
        main_data = weather_data['main']
        temperature = main_data['temp']
        humidity = main_data['humidity']
        
        weather_description = weather_data['weather'][0]['description']
        
        speak(f"The temperature in {city} is {temperature} Kelvin.")
        speak(f"The humidity is {humidity}%.")
        speak(f"The weather is {weather_description}.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")



if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

           

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = 'C:/Desktop/Videoder'
            rrr=random.randint(0,20)
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[rrr]))

        

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:/Users/jyoti kumari/AppData/Local/Programs/Microsoft VS Code/Code.exe"
            os.startfile(codePath)

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "kunalkumarnawada97087@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend kunal. I am not able to send this email")  


        elif 'tell me a joke' in query:
                tellJoke()

        elif 'translate' in query:
            speak("Sure, what would you like me to translate?")
            text_to_translate = takeCommand()

            speak("To which language should I translate it?")
            target_language = takeCommand().lower()
            
            translated_text = translateText(text_to_translate, target_language)
            print(f"Translated text: {translated_text}")
            speak(translated_text)

            # Set the voice property to the target language for speech output
            for voice in voices:
                if target_language in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break

        elif 'news' in query:
            speak("Sure, here are the latest news headlines.")
            get_news(news_api_key)
    
        elif 'weather' in query:
            speak("Sure, please tell me the city name.")
            city = takeCommand().lower()
            get_weather(weather_api_key, city)


        elif 'exit' in query:
                print("Goodbye!")
                speak("Goodbye!")
                break          
        





