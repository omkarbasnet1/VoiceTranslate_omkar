
# VoiceTranslate_omkar
***Project Sprint 2***
***Room Booking reserve***

**Student:** Omkar Basnet
**Course:** Software Engineering
            Graduate Student

## Project Overview
This project implements an AI skill set to interact with a Meeting Room Booking REST API.
it includes a Python script to connect with the server, check for available rooms and cancel reserve rooms automatically.

## Features
1. Secure Authentication logs and manages JWT bearer token
2. Room Availability , Booking Management , Cancellation and Automated testing.

## how to run locally
1. **python 3.10**
2. **FFmpeg:** Required by the OpenAI Whisper library for audio processing.
  **Windows:** ' winget install ffmpeg'.
  **Linux:** 'sudo apt-get install ffmpeg'.
  **Mac**: 'brew install ffmpeg'.

### Secrets key
This program uses .env file to keep credentials safe which has:
    SERVER_URL, USER_EMAIL and USER_PASSWORD
The workflow installs dependencies, creates a temporary .env file from the secrets

### Install dependencies:
1. pip install -r requirements.txt

### Usage
1. Run the main application:
    python Room_booking_skills.py
2. For Automated testing:
    python -m pytest tests/test_skills.py 
  


