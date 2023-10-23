import speech_recognition as sr

from models.text2speech import speak
from models.translation import translate
import threading

sr.__version__ = '3.10.0'

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def run_translation_and_t2s(text, language, volume, rate):
    print("Original Text: ", text)
    translated_text = translate(text, lang=language)
    print("Translated Text", translated_text)
    if text == translated_text:
        return False
    if translated_text:
        speak(translated_text, volume, rate)

def process_sound(language, volume=0.9, rate=150):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        try:
            audio2 = recognizer.listen(source, phrase_time_limit=5)
            if audio2.frame_data:
                original_text = recognizer.recognize_google(audio2, language="id")
                original_text = original_text.lower()
                
                translation_and_t2s = threading.Thread(
                    target=run_translation_and_t2s, args=(original_text, language, volume, rate))
                translation_and_t2s.start()
        except Exception as e:
            print("Error processing")
            print(e)
            