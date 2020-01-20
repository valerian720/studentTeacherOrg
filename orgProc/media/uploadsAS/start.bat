@echo off
%SystemRoot%\System32\reg.exe query "HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if not errorlevel 1 (start "" chrome.exe -incognito http://localhost:8000) ELSE (start http://localhost:8000)
py manage.py runserver