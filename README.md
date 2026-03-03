
# VoiceTranslate_omkar
***Project Sprint 3***
***Room Booking Voice AI agent ***

**Student:** Omkar Basnet

**Course:** Software Engineering (Graduate Student)

## Project Overview
This project is a voice activated AI agent capable of answering question about meeting room reservation.
It uses LangChain for agentic routing, Ollama running the 'granite4.1b' model for local LLM processing, and
OpenAI's Whisper for offline voice transcription.

## How It works
1. Whisper (openAI) converts your voice to text
2. LangChain routes the question to the right tools
3. Ollama runs the Ai model locally
4. Tools helps to cll the room booking API to get real data
5. AI gives you an answer

## How to Setup the AI
This project runs the AI models locally on your machine, you need to download:
1. Install Ollama: from https://ollama.com/
2. Download the Model: Open your terminal and run the following command to download:
   * '''bash
   * ollama pull granite4:1b
3. Keep ollama running while run the project

## Features
1. Secure Authentication logs and manages JWT bearer token
2. Room Availability , Booking Management , Cancellation , agent AI and Automated testing.

## how to run locally
1. **python 3.10**
2. **FFmpeg & PortAudio:** Required by the OpenAI Whisper library for audio processing adn PyAudio.
 * **Windows:**  winget install ffmpeg
 * **Linux:** sudo apt-get update && sudo apt-get install -y ffmpeg portaudio19-dev python3-pyaudio
 *  **Mac**: brew install ffmpeg portaudio
               
### Install dependencies:
1. pip install -r requirements.txt
   
### Secrets key (.env)
* It requires authentication to communicate with the room booking API.
* This program uses .env file to keep credentials safe which has:
   * SERVER_URL = "http://server" 
   * USER_EMAIL = "email@example.com" 
   * USER_PASSWORD = "password"
* The workflow installs dependencies, creates a .env file from the secrets


### running the program
1. Run the main application:
   * python main.py
   * (wait 20-30 seconds), then when you see "listening..Please Speak"
    talk into your microphone.
   * To quit : ctrl + c
   * Example: What room are free today? or Do I have any reservations tomorrow?
   
2. For Automated testing:
  * python -m pytest tests/test_integration.py -s 



