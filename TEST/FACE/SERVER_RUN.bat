@echo off


:: This batch file runs pyqum v0.1
ECHO WELCOME TO PYQUM 101

rem take current dir of this file
set "crt_dir=%~dp0"
echo Current dir:"%crt_dir%"
rem set config file name
set "config_file_name=..\..\..\path.cfg"


:: echo Config path:
:: echo Relative Config file path: %crt_dir%%config_file_name%
:: %crt_dir%%config_file_name%

rem get Fully Qualified path of CONFIGG folder
for %%I in ("%crt_dir%%config_file_name%") do set "config_FQPN=%%~fI"
echo Fully Qualified config file path: %config_FQPN%


if exist %config_FQPN% (
    echo Config file already exists
	goto read_config
) else (
    echo Config file does not exist, creating file...
)

:read_config
	for /F "tokens=1* delims=:" %%a in ('findstr "DR setting" %config_FQPN%') do (
		echo DR setting: %%b
		set "DRsetting=%%b"
	)
	for /F "tokens=1* delims=:" %%a in ('findstr "conda environment" %config_FQPN%') do (
		echo conda environment: %%b
		set "CONDAPATH=%%b"
	)


SET FLASK_APP=pyqum
SET ENVNAME=PYQUM-server-offline
call %CONDAPATH%\Scripts\activate.bat %ENVNAME%

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

:pyqum
    ::ECHO INITIATE AWG
    ::python -c "from pyqum.instrument.modular import AWG; print(AWG.InitWithOptions())"
    set /p answer=WEB Production (P1/P2), Development (D) or LOCAL (L1/L2)?
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
    if /i "%answer:~,2%" EQU "S" (
        SET FLASK_ENV=production
        echo Running WEB Production on Simulation
        goto simulation)
	if /i "%answer:~,2%" EQU "SL" (
        SET FLASK_ENV=development
        echo Running WEB Production on Simulation local
        goto simulation_local)
    goto pyqum


:development
    ECHO STARTING APP as Development Web
    python pqrun.py development 5300
    ::start server using batch command:
    ::flask run --host=127.0.0.1 --port=5200 

:production_1
    ECHO STARTING APP as Production Web on DR-1
    ECHO Environment name: %ENVNAME%

    python pqrun.py production 5301

:production_2
    ECHO STARTING APP as Production Web on DR-2
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py production 5302

:local_2
    ECHO STARTING APP as Local DMS on DR-2
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py local 5302

:local_1
    ECHO STARTING APP as Local DMS on DR-1
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py local 5301


:simulation
    ECHO STARTING APP as Production Web Simulation
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py production 5400
	
:simulation_local
    ECHO STARTING APP as Local Web Simulation
    ECHO Environment name: %ENVNAME%
    call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
    python pqrun.py local 5400
PAUSE

