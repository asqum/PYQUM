:: Installing PYQUM 101 on WIN10 for DR-A

@echo off

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
:: set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%

ECHO Installing PYQUM 101
pip install -e .

:: ATS-9371 SDK
ECHO Installing ATS-API
cd C:\AlazarTech\ATS-SDK\7.4.0\Samples_Python\Library
pip install -e .

:: Resonator tool
ECHO Installing Resonator tool
cd C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\BETAsite\resonator_tools
pip install -e .

:: qspp
ECHO Installing QuData Post-Processing
cd C:\Users\ASQUM\Documents\GitHub\PYQUM\TEST\BETAsite\Signal_Processing
pip install -e .




PAUSE