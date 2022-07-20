:: Installing FLASKAPP 101

@echo off

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%

ECHO Installing PYQUM 101
pip install -e .

PAUSE