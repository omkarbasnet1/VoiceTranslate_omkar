
# VoiceTranslate_omkar AI Voice-to-text (Project Sprint 4)
***Room Booking Agent ***

**Student:** Omkar Basnet
**Course:** Software Engineering (Graduate Student)

***Deployed Server:***  http://167.71.178.212:8000

## Project Overview
This project is an intelligent, voice-activated desktop client (`ai_agent.py`) that interacts with a remote Django REST API (`Room_booking_serve`) to manage meeting room reservations. Users can use natural language voice commands to check room availability, book rooms, and manage their schedule. 

The project features a full Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions, ensuring code quality and automated deployment to a production Linux server.

--- 
## System Architecture
The project is divided into two main components:

1. **The AI Voice Client (Local):** A Python-based GUI application that uses system audio to capture speech, processes it into text, and sends RESTful HTTP requests to the backend server.
2. **The Django API Server (Remote):** A backend server application that manages the SQLite3 database, handles user authentication, and processes booking logic.

---

## Linux Server Deployment Overview
This project does **not** install system-wide Python packages. It uses a strictly isolated deployment strategy:

* **Application Directory:** Deploys to (`/opt/Room_booking_serve`).
* **Environment Isolation:** Creates and utilizes a Python Virtual Environment (`venv/`) to contain all dependencies.
* **Database:** Utilizes a local `db.sqlite3` file (no heavy external database servers like PostgreSQL required).
* **Process Management:** The server runs in the background using `gunicorn` on port `8000`, managed either via `nohup` (in the CI/CD script) or as a dedicated `systemd` background service (`roombooking.service`).
* **Security:** Configured to accept traffic via Django's `ALLOWED_HOSTS` configuration, with sensitive credentials injected securely via `.env` files.

---

## CI/CD Pipeline (github Actions)
**The Pipeline executes the following steps:**
1. **Environment Setup:** Provisions an Ubuntu runner and installs system dependencies (`ffmpeg`, `portaudio19-dev`).
2. **Dependency Installation:** Installs Python requirements from `requirements.txt`.
3. **Linting (`flake8`):** Scans the local client code for syntax errors and complexity warnings (explicitly ignoring the Django server folder to prevent third-party code linting failures).
4. **Automated Testing (`pytest`):** Injects mock environmental secrets and runs the test suite (`tests/`) to verify API connectivity and login functionality.
5. **Automated SSH Deployment:** If all tests pass, the pipeline securely SSH's into the target Linux Droplet, pulls the latest code, updates the virtual environment, and restarts the backend server.

---

## Local Client Setup and Installation
To run the Voice-to-Text AI Agent locally, ensure you have Python 3.10+ installed.

### 1. Install System Audio Dependencies
Because the client relies on microphone access, you must have the following system dependencies installed:
* **Windows:** Usually works out of the box with `pip install pyaudio`.
* **Linux (Ubuntu/Debian):** `sudo apt-get install ffmpeg portaudio19-dev`
* **Mac (Homebrew):** `brew install portaudio ffmpeg`

### 2. Install Python Dependencies
Open your terminal in the root directory and run:
    ```bash 
    pip install -r requirements.txt

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

   
### Secrets key (.env)
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
2. Room Manager GUI ( sprint 4) Application
   * python gui.py
   * add rooms, update capacity, remove roooms: Saves cancellation_report.txt
   * or python ai_agent.py (if you wanna voice char with AI)
     
3. API function ( sprint 2)
   * python Room_bookings_skills.py

4. python ai_agent.py
   * Example: What room are free today? or Do I have any reservations tomorrow?
   * Book a room C for tomorrow or any free date ?
   * To quit : ctrl + c

   
### For Automated testing:
1. Sprint 4 Tests
   *  pytest  tests/test_db_manager.py
2. for other tests
   * pytest  tests/test_skills.py
   * pytest  tests/test_integration.py
   * pytest  tests/test_transcription.py 



