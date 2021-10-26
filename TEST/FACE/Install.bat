:: Installing FLASKAPP 101

@echo off

:: Initialize Anaconda Environment
:: set root=C:\ProgramData\Anaconda3
:: call %root%\Scripts\activate.bat %root%
rem Define here the path to your conda installation
set CONDAPATH=C:\Users\ASQUM\anaconda3
rem Define here the name of the environment
::set ENVNAME=base
set ENVNAME=PYQUM-server

rem Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
ECHO call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
call %CONDAPATH%\Scripts\activate.bat %ENVNAME%

ECHO Installing PYQUM 101
pip install -e .

PAUSE