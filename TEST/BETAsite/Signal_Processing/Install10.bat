:: Installing Qum Data Post-Processing module

@echo off

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
:: set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%

ECHO Installing QuData Post-Processing
pip install -e .

PAUSE