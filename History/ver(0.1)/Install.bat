:: Installing PyQuM v0.1

@echo off

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%

ECHO Installing PyQuM v0.1
pip install -e .

PAUSE