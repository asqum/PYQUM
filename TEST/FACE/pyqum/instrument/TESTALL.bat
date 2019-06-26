:: This batch file runs TESTALL

@echo off
:: Start Windows batch file maximized
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b

ECHO TESTING ALL MODULES
::DIR

:: Initialize Anaconda Environment
:: set root=C:\ProgramData\Anaconda3
set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%
::call conda list flask
cd %cd%
python TESTALL.py

PAUSE
