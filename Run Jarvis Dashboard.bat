@echo off
title Jarvis Dashboard Launcher
echo Starting Jarvis Backend...
start "Jarvis Backend" cmd /k "python backend/server.py"
timeout /t 2 >nul
echo Starting Jarvis Dashboard...
cd jarvis-dashboard
npm run dev
pause
