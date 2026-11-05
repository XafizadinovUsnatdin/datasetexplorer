@echo off
title Dataset Explorer AI Launcher
chcp 65001 >nul

echo ================================================================
echo               📊 DATASET EXPLORER AI LAUNCHER
echo ================================================================
echo Loyiha manzili: %~dp0
echo.

cd /d "%~dp0"

:: 1. Check Python
set PY_CMD=
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PY_CMD=python
) else if exist "C:\Users\GIGABAYTE\anaconda3\python.exe" (
    set PY_CMD="C:\Users\GIGABAYTE\anaconda3\python.exe"
) else (
    echo [XATOLIK] Python tizimda topilmadi!
    echo Iltimos, Python yoki Anaconda o'rnatilganligini tekshiring.
    pause
    exit /b 1
)

echo Python topildi: %PY_CMD%
echo Streamlit server ishga tushirilmoqda...
echo.
echo Brauzer avtomatik ochilishi kerak: http://localhost:8501
echo Serverni to'xtatish uchun ushbu oynada [Ctrl + C] tugmalarini bosing.
echo ================================================================
echo.

%PY_CMD% -m streamlit run app.py --server.port 8501

if %ERRORLEVEL% neq 0 (
    echo.
    echo [XATOLIK] Ilovani ishga tushirishda xatolik yuz berdi.
    pause
)

