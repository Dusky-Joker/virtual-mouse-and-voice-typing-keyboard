import speech_recognition as sr
import pyttsx3


class voiceDetector:
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)

    def detectVoice(self):
        with self.mic as source:
            try:
                self.engine.say("You can speak now. I am Listening...")
                self.engine.runAndWait()
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
                self.engine.say("Recognizing...")
                self.engine.runAndWait()
                text = self.r.recognize_google(audio)

                if text == 'stop listening' or text[-14:] == 'stop listening' or text == 'quit' or text[-4:] == 'quit':
                    self.engine.say("Quiting the program")
                    self.engine.runAndWait()
                    return True
                return text
            except:
                self.engine.say("Can't recognize your audio. Please try speaking in quiet environment")
                self.engine.runAndWait()
                return False
