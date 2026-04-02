@echo off
title Backend Server - Autism Stress Detection
color 0B

echo ========================================
echo   Backend Server - FastAPI
echo ========================================
echo.
echo Starting server on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

cd /d "%~dp0"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
