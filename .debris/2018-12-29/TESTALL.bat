:: This batch file runs TESTALL

@echo off

ECHO TESTING ALL INSTRUMENTS
::DIR

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%
::call conda list flask
cd %cd%
python TESTALL.py

PAUSE
