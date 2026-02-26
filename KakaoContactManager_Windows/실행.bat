@echo off
chcp 65001 >nul
echo 카카오톡 연락처 관리 도구 실행 중...

REM Python 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python이 설치되지 않았습니다.
    echo https://python.org 에서 Python 3.8 이상을 설치해주세요.
    pause
    exit /b
)

REM 패키지 설치
echo 필요한 패키지 설치 중...
pip install -r requirements.txt

REM 프로그램 실행
echo 프로그램 시작...
python kakao_contact_manager_gui.py

pause
