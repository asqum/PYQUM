:: This batch file runs pyqum v0.1

@echo off
:: Start Windows batch file maximized
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b

ECHO WELCOME TO PYQUM 101
::DIR

:: Initialize Anaconda Environment
set root=C:\ProgramData\Anaconda3
::set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%
::call conda list flask
SET FLASK_APP=pyqum
SET FLASK_ENV=development

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
        echo Think about it
        goto tq)
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
    set /p answer=WEB or LOCAL (W/L)?
    if /i "%answer:~,1%" EQU "W" (
        echo Running WEB
        goto web)
    if /i "%answer:~,1%" EQU "L" (
        echo Running LOCAL
        goto local)
    echo Please type W for Web or L for Local
    goto pyqum

:local
    ECHO STARTING APP as Local
    python pqrun.py local
    goto tq

:web
    ECHO STARTING APP as Web Server
    python pqrun.py web
    ::start server using batch command:
    ::flask run --host=127.0.0.1 --port=5200 
    ::the above method will make AWG's initialization depends on VSA's
    goto tq

:tq
    ECHO Thank you :)

PAUSE
