import speech_recognition as sr
import pyttsx3

if __name__ == "__main__":
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    r = sr.Recognizer()

    speak("Hello, I am Gipsy")

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        print("Recognizing...")
        