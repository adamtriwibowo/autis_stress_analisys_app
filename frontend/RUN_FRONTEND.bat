@echo off
title FRONTEND - Autism Stress Detection
color 0A
cls

echo.
echo ================================================================
echo           FRONTEND - Autism Stress Detection
echo ================================================================
echo.
echo   Aplikasi akan terbuka di: http://localhost:3000
echo.
echo   Pastikan BACKEND sudah berjalan sebelum menggunakan!
echo ================================================================
echo.

cd /d "%~dp0"

npm start

pause
