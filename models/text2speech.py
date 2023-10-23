import pyttsx3 as tts
tts.__version__ = '2.90'


def speak(text, volume=0.9, rate=150, lang="en"):
    engine = tts.init()
    engine = properties(engine, volume, rate, lang)    
    engine.say(text)
    engine.runAndWait()
    
def properties(engine, volume, rate, lang):
    #Change Properties of text to speech
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)
    engine.setProperty('voice', str(lang))
    return engine
