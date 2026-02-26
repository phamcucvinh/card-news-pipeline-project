@echo off
set CHROME="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
set DATA_DIR="%TEMP%\chrome_dev_profile"

start "" %CHROME% --disable-web-security --disable-site-isolation-trials --user-data-dir=%DATA_DIR% http://127.0.0.1:7860
