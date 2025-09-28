@echo off
REM run.bat - Windows batch file to run the ML Model Evaluator

REM Make sure we're in the right directory
cd /d "%~dp0"

REM Execute the main Python script with all arguments
python main.py %*
