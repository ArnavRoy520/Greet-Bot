import pyttsx3


def speak(text):
    global pyobj
    pyobj.say(text)
    pyobj.runAndWait()


pyobj = pyttsx3.init()
pyobj.setProperty("rate",125)
voices = pyobj.getProperty("voices")
pyobj.setProperty("voice",voices[1].id)