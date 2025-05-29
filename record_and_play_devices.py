import sounddevice as sd
import soundfile as sf
import os
import time
import threading
import numpy as np

# Text to audio packages
import pyttsx3

SHARED_DIR = './shared_audio'
INPUT_FILE = os.path.join(SHARED_DIR, 'input.wav')
OUTPUT_FILE = os.path.join(SHARED_DIR, 'output.txt')

SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 3  # seconds

def record_audio(stop_event, audio_buffer):
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32') as stream:
        print("Recording started. Press Enter to stop.")
        while not stop_event.is_set():
            data, _ = stream.read(1024)
            audio_buffer.append(data)

while True:

    # Wait for container to process and output result
    if not os.path.exists(INPUT_FILE):

        input("Press Enter to start recording...")
        stop_event = threading.Event()
        audio_buffer = []

        record_thread = threading.Thread(target=record_audio, args=(stop_event, audio_buffer))
        record_thread.start()

        input()  # Wait for Enter to stop recording
        stop_event.set()
        record_thread.join()

        audio = np.concatenate(audio_buffer, axis=0)
        sf.write(INPUT_FILE, audio, SAMPLE_RATE)
        print(f"Recording stopped and saved to {INPUT_FILE}\n")
        

    # Wait for container to process and output result
    while not os.path.exists(OUTPUT_FILE):
        time.sleep(0.1)

    print(f"Playing {OUTPUT_FILE}")

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
        llm_response = file.read()

    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.voice.compact.ja-JP.Kyoko')
    engine.say(llm_response)
    engine.runAndWait()
    
    #processed_audio, fs = sf.read(INPUT_FILE)
    #sd.play(processed_audio, fs)
    #sd.wait()

    # Clean up for next round
    os.remove(OUTPUT_FILE)
    print("Loop complete. Recording again...\n")
