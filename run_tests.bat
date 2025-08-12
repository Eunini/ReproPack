@echo off
echo Running ReproPack API Tests...
echo.
echo Make sure the API server is running first by running start_server.bat
echo.

cd /d "%~dp0"
C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe test_api.py

echo.
echo Test completed. Press any key to exit...
pause
