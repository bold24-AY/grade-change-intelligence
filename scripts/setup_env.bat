@echo off
echo ===================================================
echo Setting up Grade Change Intelligence Environment
echo ===================================================

cd "%~dp0\.."

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.11+.
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment (venv)...
    python -m venv venv
) else (
    echo Virtual environment (venv) already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Environment setup completed successfully!
pause
