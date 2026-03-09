import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from openai import OpenAI

client = OpenAI(api_key="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)")

if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    r = sr.Recognizer()

    def ask_ai(question):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=question
        )
        return response.output_text

    def processcommand(c):
        if "open youtube" in c:
            webbrowser.open("https://www.youtube.com")
        elif "open google" in c:
            webbrowser.open("https://www.google.com")
        elif "open facebook" in c:
            webbrowser.open("https://www.facebook.com")
        elif "open instagram" in c:
            webbrowser.open("https://www.instagram.com")
        elif "open github" in c:
            webbrowser.open("https://www.github.com")
        else:
            print("Asking AI...")
            answer = ask_ai(c)
            print(answer)
            speak(answer)


    speak("Hello, I am Gipsy")

    while True:

        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)

                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            word = r.recognize_google(audio).lower()
            print(f"You said: {word}")
        
            if "gipsy" in word:
                speak("Yes, how can I help you?")
                print("gipsy is activated")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio).lower()

                    processcommand(command)
    
        except sr.WaitTimeoutError:
            print("No speech detected")

        except sr.UnknownValueError:
            print("Could not understand audio")
        
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")

        except Exception as e:
            print(f"An error occurred: {e}")