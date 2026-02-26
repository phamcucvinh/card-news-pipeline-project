@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
playwright install
echo.
echo 설치 완료! 실행 방법:
echo   venv\Scripts\activate
echo   python app.py
pause
