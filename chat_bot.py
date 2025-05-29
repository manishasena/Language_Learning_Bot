import os
import time
import yaml
#####
# Audio recording packages
#import pyaudio
import wave
import math

# Audio to text packages
import whisper

# LLM packages
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Text to audio packages
#import pyttsx3

# Kanji to hiragana or katakana
import pykakasi
#####

# Read the YAML file
with open('parameters.yml', 'r') as file:
    parameters = yaml.safe_load(file)

#SHARED_DIR = '/app/shared' #'./shared_audio' #
#INPUT_FILE = os.path.join(SHARED_DIR, 'input.wav')
#OUTPUT_FILE = os.path.join(SHARED_DIR, 'output.txt')

class LanguageBot():
    def __init__(self, parameters):
        
        # Set language
        self.language = parameters['language']
        self.hiragana_mode = parameters['hiragana']

        # If Japanaese, check if hiragana conversion needed:
        if self.language == "Japanese":
            if self.hiragana_mode:
                # Initalise model to convert response to hiragana
                self.kks = pykakasi.kakasi()

        # Load Audio to Text Model
        self.whisper_model = whisper.load_model(parameters['whisper_model'])

        # Load LLM
        ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.LLM_model = OllamaLLM(model=parameters['OllamaLLM_model'], base_url=ollama_url)
        #self.LLM_model = OllamaLLM(model = "gemma3:1b")

        # Locations of input, output and conversation history files
        self.INPUT_FILE = parameters['INPUT_FILE']
        self.OUTPUT_FILE = parameters['OUTPUT_FILE']
        self.CONVERSATION_HISTORY = parameters['CONVERSATION_HISTORY']

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

        input_audio = self.INPUT_FILE 
        input_language = self.language

        # Transcribe the recording in original language
        transcription = self.whisper_model.transcribe(input_audio)

        # Translate the recording from original language to English
        translation = self.whisper_model.transcribe(input_audio, language = input_language, task = "translate")

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
        
        print('Running text to audio')
        engine = pyttsx3.init()
        if self.language == "Japanese":
            engine.setProperty('voice', 'com.apple.voice.compact.ja-JP.Kyoko')
        elif self.language == "German":
            engine.setProperty('voice', 'com.apple.eloquence.de-DE.Flo')

        engine.save_to_file(llm_response, self.OUTPUT_FILE)
        #engine.say(llm_response)
        engine.runAndWait()

    def run_chatbot(self):

        # Initialise Prompt Template
        self.prompt_template()
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.LLM_model

        
        print(f"Welcome to the {self.language} learning Chatbot.")
        self.context = ""
        while True:
            if os.path.exists(self.INPUT_FILE):

                # Transcribe and translate user input
                user_input, translation = self.audio_to_text() #input("User: ")

                # Delete input file
                os.remove(self.INPUT_FILE)

                print("User: ", translation['text'], user_input['text'])
                
                # Prompt the LLM
                result = chain.invoke({"language": self.language, "context": self.context, "question": user_input['text']})

                # Check if response should be returned in hirgana
                if self.hiragana_mode:
                    result = self.kks.convert(result)
                    result = ''.join([item['hira'] for item in result])
                print("Bot: " + result)

                # Write bot response to a text file
                with open(self.OUTPUT_FILE, "w") as file:
                    file.write(result)

                # Append response to conversation history
                self.context += f"\nUser: {user_input['text']}\n AI: {result}"

                # Write conversation so far to text file
                with open(self.CONVERSATION_HISTORY, "w") as file:
                    file.write(self.context)
            else:
                time.sleep(1)


language_bot = LanguageBot(parameters)
language_bot.run_chatbot()