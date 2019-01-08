:: This batch file runs TEST ENA

@echo off

ECHO TESTING ENA REMOTELY
::DIR

:: Initialize Anaconda Environment
:: set root=C:\ProgramData\Anaconda3
:: call %root%\Scripts\activate.bat %root%

::call conda list flask

cd %cd%
python ENA_Test.py

PAUSE
