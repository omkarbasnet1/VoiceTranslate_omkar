
# VoiceTranslate_omkar
***Project Sprint 4***
***Room Booking Voice AI agent ***

**Student:** Omkar Basnet

**Course:** Software Engineering (Graduate Student)

***Deployed Server:***  http://167.71.178.212:8000

## Project Overview
This project is a voice activated AI agent capable of answering question about meeting room reservation.
It uses LangChain for agentic routing, Ollama running the 'granite4.1b' model for local LLM processing, and
OpenAI's Whisper for offline voice transcription.
1. Voice AI agent (Sprint 3) - ask question about bookings using voice
2. Desktop GUI ( Sprint 4) - Manage rooms through a visual interface
3. REST API client (Sprint 2) 

## Technology
1. Whisper (openAI) converts your voice to text
2. GUI: TKinter (Python built-in)
3. AI agent: LangChain + Ollama(granite4:1b model)
4. Database: SQLite3
5. Server: REST framework(deployed on Digital Ocean)
6. CI/CD : GitHub action

## How to Setup the AI
This project runs the AI models locally on your machine, you need to download:
1. Install Ollama: from https://ollama.com/
2. Download the Model: Open your terminal and run the following command to download:
   * '''bash
   * ollama pull granite4:1b
3. Keep ollama running while run the project

## Features of sprint 4 
1. GUI application: add, update and delete rooms
2. Cancellation Reports
3. Database Functions
4. Deployed Server
5. CI/CD Pipeline

## how to run locally
1. **python 3.10**

2. **FFmpeg:** Required by the OpenAI Whisper library for audio processing.
  **Windows:** ' winget install ffmpeg'.
  **Linux:** 'sudo apt-get install ffmpeg'. sudo apt-get install -y ffmpeg portaudio19-dev python3-pyaudio
  **Mac**: 'brew install ffmpeg'.
3. **pyaudio**: 'brew install ffmpeg portaudio'
               
### Install dependencies:
1. pip install -r requirements.txt
   
### Secrets key (.env)
* It requires authentication to communicate with the room booking API.
* This program uses .env file to keep credentials safe which has:
   * SERVER_URL = "http://167.71.178.212:8000" 
   * USER_EMAIL = "email@example.com" 
   * USER_PASSWORD = "password"
* The workflow installs dependencies, creates a .env file from the secrets


### running the program
1. Run the main application:
   * python main.py
   * (wait 20-30 seconds), then when you see "listening..Please Speak"
    talk into your microphone.
     * To quit : ctrl + c
2. Room Manager GUI ( sprint 4)
   * python gui.py
   * add rooms, update capacity, remove roooms: Saves cancellation_report.txt
     
3. API function ( sprint 2)
   * python Room_bookings_skills.py

4. python ai_agent.py
   * Example: What room are free today? or Do I have any reservations tomorrow?
   * To quit : ctrl + c

   
### For Automated testing:
1. Sprint 4 Tests
   *  pytest -m tests/test_db_manager.py
2. for other tests
   * pytest -m tests/test_skills.py
   * pytest -m tests/test_integration.py
   * pytest -m tests/test_transcription.py 



