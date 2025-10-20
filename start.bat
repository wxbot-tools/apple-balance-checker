@echo off
chcp 65001 >nul
echo ==========================================
echo   Apple Balance Checker 启动脚本
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python！
    echo 请先安装Python 3.10.12
    echo 下载地址: https://www.python.org/downloads/release/python-31012/
    echo.
    pause
    exit /b 1
)

REM 检查Python版本
echo [1/4] 检查Python版本...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
set REQUIRED_VERSION=3.10.12

echo 当前Python版本: %PYTHON_VERSION%
echo 要求Python版本: %REQUIRED_VERSION%

if not "%PYTHON_VERSION%"=="%REQUIRED_VERSION%" (
    echo.
    echo [错误] Python版本不匹配！
    echo 本程序要求Python版本为 3.10.12
    echo 当前版本为 %PYTHON_VERSION%
    echo.
    echo 请安装正确的Python版本:
    echo https://www.python.org/downloads/release/python-31012/
    echo.
    pause
    exit /b 1
)
echo ✓ Python版本检查通过
echo.

REM 检查Chrome是否安装
echo [2/4] 检查Chrome浏览器...
set CHROME_INSTALLED=0

REM 检查常见的Chrome安装路径
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1

if %CHROME_INSTALLED%==1 (
    echo ✓ 检测到Chrome浏览器
) else (
    echo [警告] 未检测到Chrome浏览器！
    echo.
    
    REM 检查是否存在ChromeSetup.exe
    if exist "ChromeSetup.exe" (
        echo 发现ChromeSetup.exe，正在安装Chrome...
        echo 请按照安装向导完成Chrome浏览器的安装
        echo.
        start /wait ChromeSetup.exe
        
        REM 安装后再次检查
        if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_INSTALLED=1
        
        if %CHROME_INSTALLED%==1 (
            echo ✓ Chrome安装成功
        ) else (
            echo [错误] Chrome安装失败或未完成
            echo 请手动安装Chrome浏览器后重试
            echo 下载地址: https://www.google.com/chrome/
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo [错误] 未找到ChromeSetup.exe安装文件
        echo.
        echo 请执行以下操作之一：
        echo 1. 将ChromeSetup.exe放在当前目录下，然后重新运行此脚本
        echo 2. 手动安装Chrome浏览器: https://www.google.com/chrome/
        echo.
        pause
        exit /b 1
    )
)
echo.

REM 检查依赖
echo [3/3] 检查Python依赖...
pip show tornado >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    echo ✓ 依赖安装完成
) else (
    echo ✓ 依赖包已安装
)
echo.

REM 启动应用
echo ==========================================
echo   启动 Web 服务器...
echo ==========================================
echo.
echo 服务器启动后会自动打开浏览器
echo 默认地址: http://localhost:8080/view/index.html
echo 按 Ctrl+C 可停止服务器
echo.
echo ==========================================
echo.

python web_app.py

echo.
echo 服务器已停止
pause

