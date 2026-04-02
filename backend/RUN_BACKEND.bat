@echo off
title BACKEND SERVER - Autism Stress Detection
color 0B
cls

echo.
echo ================================================================
echo           BACKEND SERVER - Autism Stress Detection
echo ================================================================
echo.
echo   Server akan berjalan di: http://127.0.0.1:8000
echo.
echo   JANGAN TUTUP WINDOW INI saat menggunakan aplikasi!
echo ================================================================
echo.

cd /d "%~dp0"

python simple_server.py

pause
