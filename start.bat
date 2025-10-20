@echo off
chcp 65001 >nul
echo ==========================================
echo   Apple Balance Checker
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR - Python not found!
    echo Please install Python 3.10.12
    echo Download: https://www.python.org/downloads/release/python-31012/
    echo.
    pause
    exit /b 1
)

REM Check Python version
echo Step 1/3 - Checking Python version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
set REQUIRED_VERSION=3.10.12

echo Current Python version: %PYTHON_VERSION%
echo Required version: %REQUIRED_VERSION%

if not "%PYTHON_VERSION%"=="%REQUIRED_VERSION%" (
    echo.
    echo ERROR - Python version mismatch!
    echo This program requires Python 3.10.12
    echo Current version: %PYTHON_VERSION%
    echo.
    echo Please install the correct version:
    echo https://www.python.org/downloads/release/python-31012/
    echo.
    pause
    exit /b 1
)
echo OK - Python version check passed
echo.

REM Check Chrome browser
echo Step 2/3 - Checking Chrome browser...
set CHROME_INSTALLED=0

REM Check common Chrome installation paths
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1

if %CHROME_INSTALLED%==1 (
    echo OK - Chrome browser detected
) else (
    echo WARNING - Chrome browser not detected!
    echo.
    
    REM Check for ChromeSetup.exe
    if exist "ChromeSetup.exe" (
        echo Found ChromeSetup.exe, installing Chrome...
        echo Please follow the installation wizard
        echo.
        start /wait ChromeSetup.exe
        
        REM Check again after installation
        if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        
        if %CHROME_INSTALLED%==1 (
            echo OK - Chrome installation successful
        ) else (
            echo ERROR - Chrome installation failed
            echo Please install Chrome manually
            echo Download: https://www.google.com/chrome/
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo ERROR - ChromeSetup.exe not found
        echo.
        echo Please do one of the following:
        echo 1. Put ChromeSetup.exe in the current directory
        echo 2. Install Chrome manually: https://www.google.com/chrome/
        echo.
        pause
        exit /b 1
    )
)
echo.

REM Check dependencies
echo Step 3/3 - Checking Python dependencies...
pip show tornado >nul 2>&1
if errorlevel 1 (
    echo Installing Python packages...
    pip install -r requirements.txt
    echo OK - Dependencies installed
) else (
    echo OK - Dependencies already installed
)
echo.

REM Start application
echo ==========================================
echo   Starting Web Server...
echo ==========================================
echo.
echo Index URL: http://localhost/view/index
echo Press Ctrl+C to stop the server
echo.
echo ==========================================
echo.

python web_app.py

echo.
echo Server stopped
pause
