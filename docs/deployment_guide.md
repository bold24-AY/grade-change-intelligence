# Deployment Guide - Grade Change Intelligence

This guide outlines deployment options for shipping the Grade Change Intelligence system to a staging or production server.

---

## 🐋 1. Containerized Deployment (Recommended)

The easiest deployment strategy uses **Docker Compose** to run the backend FastAPI microservice and frontend dashboard client.

### Prerequisites
- Install **Docker** and **Docker Compose** on the host server.

### Configuration Files
- **[Dockerfile.backend](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/Dockerfile.backend)**: Multi-stage lightweight python setup.
- **[Dockerfile.frontend](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/Dockerfile.frontend)**: Builds Streamlit frontend environments.
- **[docker-compose.yml](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/docker-compose.yml)**: Glues the components, routes networks, and mounts volume folders.

### Spin up the Stack
To build and launch the containers:
```bash
docker-compose up -d --build
```
This boots:
- **FastAPI API Server**: Port `8000` (mapped locally).
- **Streamlit Command Center**: Port `8501` (mapped locally).

To stop the containers:
```bash
docker-compose down
```

---

## 💻 2. Windows Service Deployment

In some paper mills, applications are deployed directly on Windows server workstations as background services without Docker.

### Using NSSM (Non-Sucking Service Manager)
1.  Download `NSSM` and place it in your path.
2.  Install the FastAPI backend service:
    ```cmd
    nssm install GradeChangeBackend "C:\path\to\grade-change-intelligence\venv\Scripts\python.exe" "-m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
    ```
3.  Install the Streamlit frontend service:
    ```cmd
    nssm install GradeChangeDashboard "C:\path\to\grade-change-intelligence\venv\Scripts\streamlit.exe" "run frontend/app.py --server.port 8501"
    ```
4.  Start services:
    ```cmd
    nssm start GradeChangeBackend
    nssm start GradeChangeDashboard
    ```

---

## 🔒 3. Production Hardening Checklist
- **Database Mounting**: In production, ensure the `data/` folder is mounted as a persistent volume so that processed metrics and model registries are not lost when containers restart.
- **Port Security**: Block public access to port `8000` and `8501`. Route requests through a reverse proxy like **Nginx** or **IIS** with HTTPS enabled.
- **Worker Configuration**: In `config.yaml`, scale up Uvicorn workers to `4` or more to support parallel operator request streams.
