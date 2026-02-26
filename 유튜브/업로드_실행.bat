@echo off
chcp 65001 > nul
echo ==========================================
echo   YouTube 업로더 실행
echo ==========================================
echo.

REM Python 확인
python --version > nul 2>&1
if errorlevel 1 (
    echo Python이 설치되어 있지 않습니다.
    echo https://python.org 에서 Python을 설치해주세요.
    pause
    exit /b
)

REM 필요한 패키지 설치
echo 필요한 패키지 확인 중...
pip install selenium webdriver-manager --quiet

REM 스크립트 실행
cd /d "%~dp0"
python youtube_upload_chrome.py

pause
