@echo off
chcp 65001 >nul
cls
echo ===============================================
echo    Minimal Diary - 설치
echo ===============================================
echo.
echo 의존성 패키지를 설치합니다...
echo 시간이 1-2분 정도 걸릴 수 있습니다.
echo.

npm install

if errorlevel 1 (
    echo.
    echo [오류] 설치 실패
    pause
    exit /b 1
)

echo.
echo ===============================================
echo    설치 완료!
echo ===============================================
echo.
echo 이제 run.bat을 실행하여 앱을 시작하세요.
echo.
pause
