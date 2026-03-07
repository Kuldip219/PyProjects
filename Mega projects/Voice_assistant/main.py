import speech_recognition as sr
import pyttsx3

if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    