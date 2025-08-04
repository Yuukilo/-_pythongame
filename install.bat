@echo off
chcp 65001 >nul
echo ========================================
echo Snake Game - Anime Edition Install Script
echo ========================================
echo.
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found!
    echo Please install Python 3.7 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python environment check passed!
echo.
echo Installing game dependencies...
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Installation completed!
    echo ========================================
    echo.
    echo Run game: python main.py
    echo Or run directly: SnakeGame-AnimeEdition.exe
    echo.
) else (
    echo.
    echo Installation failed! Please check network or Python environment
)

echo Press any key to exit...
pause >nul