:: Installing PYQUM 101 on WIN10

@echo off

:: Initialize Anaconda Environment
:: set root=C:\ProgramData\Anaconda3
set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%

ECHO Installing PYQUM 101
pip install -e .

PAUSE