:: This batch file runs pyqum v0.1

@echo off
:: Start Windows batch file maximized
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b

ECHO WELCOME TO PYQUM 101
::DIR

:: Initialize Anaconda Environment
:: set root=C:\ProgramData\Anaconda3
set root=C:\Users\Great\Anaconda3
call %root%\Scripts\activate.bat %root%
::call conda list flask
SET FLASK_APP=pyqum
SET FLASK_ENV=development

IF EXIST "instance\pyqum.sqlite" (
    ECHO Database Found
) ELSE (
    flask init-db
    ECHO New Database Created
    )

::BYPASS to WEB
REM goto web
goto local

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

:local
    ECHO STARTING APP as Web Server
    python pqrun.py local
    ::start server using batch command:
    ::flask run --host=127.0.0.1 --port=5200 
    ::the above method will make AWG's initialization depends on VSA's
    goto tq

:tq
    ECHO Thank you :)

PAUSE
