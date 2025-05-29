Code for Language Bot (light weight) to support langage conversation.

Currently designed for Japanese conversation.

**Objective:** To be able to run locally on computer OR Raspberry Pi.

Due to issues with recording and playing audio within the Docker Container, this portion of the application is run in a script outside of the container.

To run:

1. Packages needed:
```
sounddevice
soundfile
numpy
```

2. First run:
`docker-compose up --build`

3. Run:
`python record_and_play_devices.py`

![Language Bot Framework](Documentation/LanguageBotFramework.png)