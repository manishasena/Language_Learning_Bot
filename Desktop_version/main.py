"""
Language Chat Bot
Date: April 2025
"""

# Have Ollama application open

# Audio recording packages
import pyaudio
import wave
import math

# Audio to text packages
import whisper

# LLM packages
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Text to audio packages
import pyttsx3

# Kanji to hiragana or katakana
import pykakasi

class LanguageBot():
    def __init__(self, language):
        
        self.language = language
        self.prompt_template()

    def mic_to_audio(self):
        """
        Recording microphone input from user into a .wav file
        """
        print('000')
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "recordedFile.wav"
        device_index = 2
        audio = pyaudio.PyAudio()

        print('1A')

        """
        print("----------------------record device list---------------------")
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
                if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

        print("-------------------------------------------------------------")
        """
        index = 0 #int(input())
        #print("recording via index "+str(index))
        print('2B')

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index = index,
                        frames_per_buffer=CHUNK)
        print ("recording started")
        Recordframes = []

        for i in range(0, math.ceil(RATE / CHUNK * RECORD_SECONDS)):
            #print(i)
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print ("recording stopped")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()

    def audio_to_text(self):
        """
        Converting .wav input into text
        """

        print("Starting mic to audio")
        self.mic_to_audio()
        print("Mic to audio complete")

        model = whisper.load_model("base")
        input_audio = self.WAVE_OUTPUT_FILENAME
        input_language = self.language

        # Transcribe the recording in original language
        transcription = model.transcribe(input_audio)

        # Translate the recording from original language to English
        translation = model.transcribe(input_audio, language = input_language, task = "translate")

        return transcription, translation

    def prompt_template(self):
        """
        Prompt template for LLM
        """

        if self.language == "Japanese":
            self.template = """
            You are a bot to help a user learn Japanese. Make your converations simple to understand for a very beginner. Make your responses only in hiragana and katakana. Do not use kanji.  Keep your responses up to 2 sentences. Try to also ask a question in return.

            Here is the conversation history {context}

            Question: {question}

            Answer:
            """
        else:
            self.template = """
            You are a bot to help a user learn {language}. Make your converations simple to understand for a very beginner. Keep your responses up to 2 sentences. Try to also ask a question in return.

            Here is the conversation history {context}

            Question: {question}

            Answer:
            """

    def text_to_audio(self, llm_response):

        engine = pyttsx3.init()
        if self.language == "Japanese":
            engine.setProperty('voice', 'com.apple.voice.compact.ja-JP.Kyoko')
        elif self.language == "German":
            engine.setProperty('voice', 'com.apple.eloquence.de-DE.Flo')
        #change_voice(engine, "nl_BE", "VoiceGenderFemale")
        engine.say(llm_response)
        engine.runAndWait()

    def run_chatbot(self):

        model = OllamaLLM(model = "gemma3:1b")
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | model

        kks = pykakasi.kakasi()

        print("welcome to the AI Chatbot. Type 'exit' to quit.")
        self.context = ""
        while True:
            user_input, translation = self.audio_to_text() #input("User: ")

            print("User: ", translation['text'])
            if user_input['text'].lower() == "exit":
                break
            
            # Promot the LLM
            result = chain.invoke({"language": self.language, "context": self.context, "question": user_input['text']})
            print(result)

            # Written response in hirgana
            result_hira = kks.convert(result)
            result_hira = ''.join([item['hira'] for item in result_hira])
            print("Bot: " + result_hira)

            # Audio of LLM response
            self.text_to_audio(result)

            # Append response to conversation history
            self.context += f"\nUser: {user_input['text']}\n AI: {result_hira}"

            # Write conversation so far to text file
            with open("conversation_history.txt", "w") as file:
                file.write(self.context)

if __name__ == "__main__":
    language_bot = LanguageBot("Japanese")
    language_bot.run_chatbot()

