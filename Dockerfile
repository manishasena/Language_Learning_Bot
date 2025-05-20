
FROM python:3.11

ADD main.py .

RUN pip install wave openai-whisper langchain langchain-ollama pyttsx3
RUN apt-get update
RUN apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev -y 
#RUN apk add gcc g++
RUN apt-get install -y gcc g++
RUN pip3 install pyaudio
#RUN apt-get update
#RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
#RUN pip install pyaudio

CMD ["python", "./main.py"]

# Build
# docker build -t language_bot .

# Run
# docker run -i -t language_bot