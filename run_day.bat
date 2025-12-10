@echo off
REM Helper script to run daily solutions
REM Usage: run_day.bat 18

if "%1"=="" (
    echo Usage: run_day.bat ^<day_number^>
    exit /b 1
)

set DAY=day%1.py

if not exist "%DAY%" (
    echo Error: %DAY% not found
    exit /b 1
)

python "%DAY%"
