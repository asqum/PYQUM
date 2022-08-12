@echo off




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
	goto write_config
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
	goto build_environment


:write_config
	rem write path string into config file
	set /p DRsetting="DR setting path: "
	set /p CONDAPATH="Conda path: "
	(
		echo DR setting:%DRsetting%
		echo Conda path:%CONDAPATH%
	) > %config_FQPN%
	echo Configuration is complete 
	goto build_environment

:build_environment
    ECHO Activate conda: %CONDAPATH%\Scripts\activate.bat 
    call %CONDAPATH%\Scripts\activate.bat base
    call conda env create -f environment.yml
    goto check_database


:check_database
	IF EXIST "%DRsetting%\pyqum.sqlite" (
		ECHO Database Found 
	) ELSE (
		ECHO NO Database was found in this path
		)


:end
	PAUSE
	exit
