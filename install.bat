@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🤖 FAKE NEWS DETECTION NLP — WINDOWS INSTALLER               ║
echo ║  Author: Ussu                                                 ║
echo ║  https://github.com/issu321/NLP-Python                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [*] Verifying Python 3.10+ installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH!
    echo     Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2 delims=." %%a in ('python --version') do set PY_MINOR=%%a
if %PY_MINOR% LSS 10 (
    echo [X] Python 3.10 or higher is required for match-case support!
    pause
    exit /b 1
)

echo [OK] Python version compatible.
echo.
echo [*] Installing Python dependencies...
pip install --upgrade pip
pip install pandas numpy scikit-learn textblob nltk

echo.
echo [*] Downloading NLTK datasets...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  [OK] INSTALLATION COMPLETE!                                  ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Run the app:  python app.py                                 ║
echo ║  With dataset: python app.py dataset.csv                     ║
echo ╚══════════════════════════════════════════════════════════════╝
pause
