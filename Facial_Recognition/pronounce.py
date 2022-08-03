from gtts import gTTS
import os

def pronounce(phrase=str()):
    """pronunciation module"""
    to_pronounce = phrase # Passing the string to pronounce

    language = 'en' # Language
    myobj = gTTS(text=to_pronounce, lang=language, slow=False) # Pronunciation settings

    myobj.save("welcome.mp3") # Writing it to a file

    return os.system("mpg321 welcome.mp3") # Playing file
