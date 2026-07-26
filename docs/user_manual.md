# User Manual & Developer Guide

Welcome to the Grade Change Intelligence codebase. This guide explains how to set up, run, and develop on the system.

## Environment Requirements
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional for containerized deployment)

---

## Getting Started (Local Development)

### 1. Setup the Python Virtual Environment
Navigate to the root directory and run the setup script:
```cmd
# Windows command prompt
C:\Users\itsay\.gemini\antigravity\scratch\grade-change-intelligence> .\scripts\setup_env.bat
```
This script will:
- Create a virtual environment `venv`
- Upgrade pip
- Install all dependencies in `requirements.txt`

### 2. Start the Backend API
Activate the virtual environment and launch Uvicorn:
```cmd
venv\Scripts\activate
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to inspect the interactive Swagger API documentation.

### 3. Start the Frontend Dev Server
Navigate to the frontend folder, install dependencies, and run:
```cmd
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the web application.

---

## Running with Docker Compose
If you prefer running inside containers:
```bash
docker-compose up --build
```
This builds and starts both the FastAPI backend (on port 8000) and the React frontend (on port 3000).
