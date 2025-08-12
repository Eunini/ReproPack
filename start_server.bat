@echo off
echo Starting ReproPack API Server...
echo.
echo The server will be available at:
echo - API Documentation: http://localhost:8000/docs
echo - API Base URL: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
