
FROM python:3.11

ADD Desktop_version/main.py .

RUN pip install wave openai-whisper langchain langchain-ollama pyttsx3 pykakasi
RUN apt-get update
RUN apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev -y 
RUN apt-get install -y gcc g++
RUN pip3 install pyaudio

CMD ["python", "main.py"]

# Build
# docker build -t language_bot .

# Run
# docker run -i -t language_bot
# docker run -it --device /dev/snd language_bot