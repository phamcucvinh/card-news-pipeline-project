@echo off
chcp 65001 >nul
cls
echo ===============================================
echo    Minimal Diary - 미니멀 일기장
echo ===============================================
echo.
echo 애플리케이션을 시작합니다...
echo.

npm start

if errorlevel 1 (
    echo.
    echo [오류] 애플리케이션 실행 실패
    echo.
    echo 해결 방법:
    echo 1. npm install 실행
    echo 2. node_modules 폴더 삭제 후 재설치
    echo.
    pause
)
