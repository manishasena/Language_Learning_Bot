
FROM python:3.11-slim

COPY chat_bot.py /app/chat_bot.py
COPY parameters.yml /app/parameters.yml

RUN pip install wave openai-whisper langchain langchain-ollama pykakasi PyYAML
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

CMD ["python", "-u", "chat_bot.py"]