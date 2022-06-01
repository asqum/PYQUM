:: This batch file runs pyqum v0.1

@echo off
:: Start Windows batch file maximized
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b

ECHO WELCOME TO PYQUM 101
::DIR

:: Initialize Anaconda Environment
ECHO NO Environment
::set root=C:\ProgramData\Anaconda3
::call %root%\Scripts\activate.bat %root%
::call conda list flask
SET FLASK_APP=pyqum


::Get Parent Directory
for %%a in (%cd%) do set "p_dir=%%~dpa"
::Up many levels by 25%
for %%a in (%p_dir:~0,-25%) do set "p2_dir=%%~dpa"
echo Up until: %p2_dir%

::Check Database Existence
IF EXIST "%p2_dir%HODOR\CONFIG\pyqum.sqlite" (
    ECHO Database Found
    goto clearpycache
) ELSE (
    ECHO NO Database was found in this path
    goto dboption
    )

:dboption
    set /p answer=Create New Database (Y/N)?
    if /i "%answer:~,1%" EQU "Y" (
        flask init-db
        ECHO New Database Created)
    if /i "%answer:~,1%" EQU "N" (
        echo Think about it )
    echo Please type Y or N
    goto dboption

::Preventing PyCache::
:clearpycache
    REM ECHO Before: Prevent PyCache: %PYTHONDONTWRITEBYTECODE%
    if "%PYTHONDONTWRITEBYTECODE%"=="1" (
        echo pycache already disabled
    ) else (
        ::locally (in RAM)
        REM set PYTHONDONTWRITEBYTECODE=1
        ::globally (user specific)
        SETX PYTHONDONTWRITEBYTECODE 1
        echo pycache just fucked
    )
    REM echo After: Prevent PyCache: %PYTHONDONTWRITEBYTECODE%

REM PAUSE
::BYPASS to WEB
::goto web

:pyqum
    ::ECHO INITIATE AWG
    ::python -c "from pyqum.instrument.modular import AWG; print(AWG.InitWithOptions())"
    set /p answer=WEB Production (P1/P2), Development (D) or LOCAL (L)?
    if /i "%answer:~,2%" EQU "P1" (
        SET FLASK_ENV=production
        echo Running WEB Production on DR-1
        goto production_1)
    if /i "%answer:~,2%" EQU "P2" (
        SET FLASK_ENV=production
        echo Running WEB Production on DR-2
        goto production_2)
    if /i "%answer:~,1%" EQU "D" (
        SET FLASK_ENV=development
        echo Running WEB Development
        goto development)
    if /i "%answer:~,2%" EQU "L1" (
        SET FLASK_ENV=development
        echo Running Local on DR-1
        goto local_1)
    if /i "%answer:~,2%" EQU "L2" (
        SET FLASK_ENV=development
        echo Running Local on DR-2
        goto local_2)
    echo Please type P (Production), D (Development) or L (Local)
    goto pyqum


:development
    ECHO STARTING APP as Development Web
    python pqrun.py development 5300
    ::start server using batch command:
    ::flask run --host=127.0.0.1 --port=5200 

:production_1
    ECHO STARTING APP as Production Web on DR-1
    @echo OFF
    rem How to run a Python script in a given conda environment from a batch file.

    rem It doesn't require:
    rem - conda to be in the PATH
    rem - cmd.exe to be initialized with conda init

    rem Define here the path to your conda installation
    set CONDAPATH=C:\Users\ASQUM\anaconda3
    rem Define here the name of the environment
    ::set ENVNAME=base
    set ENVNAME=PYQUM-server-offline

    rem Activate the conda environment
    rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
    ECHO Conda path: %CONDAPATH%\Scripts\activate.bat 
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%

    rem Run a python script in that environment
    python pqrun.py production 5301

:production_2
    ECHO STARTING APP as Production Web on DR-2
    set CONDAPATH=C:\Users\ASQUM_2\anaconda3
    set ENVNAME=PYQUM-server-offline
    ECHO Conda path: %CONDAPATH%\Scripts\activate.bat 
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py production 5302

:local_2
    ECHO STARTING APP as Local DMS on DR-2
    set CONDAPATH=C:\Users\ASQUM_2\anaconda3
    set ENVNAME=PYQUM-server-offline
    ECHO Conda path: %CONDAPATH%\Scripts\activate.bat 
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py local 5302

:local_1
    ECHO STARTING APP as Local DMS on DR-1
    set CONDAPATH=C:\Users\ASQUM\anaconda3
    set ENVNAME=PYQUM-server-offline
    ECHO Conda path: %CONDAPATH%\Scripts\activate.bat 
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py local 5301


PAUSE

