"""
Text to Audio
"""

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', 'com.apple.voice.compact.ja-JP.Kyoko')
#change_voice(engine, "nl_BE", "VoiceGenderFemale")
engine.say("こんにちは！はじめまして、よろしくお願いいたします")
engine.runAndWait()

for voice in engine.getProperty('voices'):
    print(voice)

#engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file('Hello World', 'test.mp3')
#engine.runAndWait()