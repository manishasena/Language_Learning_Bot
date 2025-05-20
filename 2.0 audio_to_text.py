"""
Whisper 
https://gist.github.com/arctic-hen7/5580d5452f77d4e6b206caf90f8d73c6

OR

https://medium.com/@gokcerbelgusen/now-you-can-turn-your-raspberry-pi-into-speech-to-text-and-text-to-speech-machine-without-1318096511be
"""

import whisper

model = whisper.load_model("base")
input_audio = "recordedFile.wav"
input_language = "Japanese"

def audio_to_text_function(model, input_audio, input_language):

    # Transcribe the recording in original language
    transcription = model.transcribe(input_audio)

    # Translate the recording from original language to English
    translation = model.transcribe(input_audio, language = input_language, task = "translate")

    return transcription["text"], translation["text"]

# Run function
transcription, translation = audio_to_text_function(model, input_audio, input_language)
print(transcription)
print(translation)