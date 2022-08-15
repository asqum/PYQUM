@echo off




rem take current dir of this file
set "crt_dir=%~dp0"
echo Current dir:"%crt_dir%"

rem get root dir of this repo
set "relative_root=..\..\"
for %%I in ("%crt_dir%%relative_root%") do set "root_FQPN=%%~fI"
echo Fully Qualified root path: %root_FQPN%

rem set config file name
set "config_file_name=..\path.cfg"

rem get Fully Qualified path of CONFIGG folder
for %%I in ("%root_FQPN%%config_file_name%") do set "config_FQPN=%%~fI"
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
    goto install_package


:install_package

	set ENVNAME=PYQUM-server-offline
	call conda activate %ENVNAME%
	
	:: qspp (editable installation, files are in PYQUM)
	ECHO Installing qspp
	pip install -e ..\BETAsite\Signal_Processing

	:: pulse_generator (editable installation, files are in PYQUM)
	ECHO Installing pulse_generator
	pip install -e ..\BETAsite\pulse_generator

	:: asqpu (editable installation, files are in PYQUM)
	ECHO Installing asqpu
	pip install -e %root_FQPN%\SKILLS\asqpu

	:: state_distinguishability (editable installation, files are in PYQUM)
	ECHO Installing state_distinguishability
	pip install -e ..\BETAsite\state_distinguishability

	:: resonator_tools (editable installation, files are in PYQUM)
	ECHO Installing resonator_tools
	pip install -e ..\BETAsite\resonator_tools

	:: atsapi (normal installation, files are in MEGA)
	ECHO Installing atsapi
	:: DR1 pip install ..\..\..\..\MEGAsync\MANUALS\DAC_ADC\AlazarTech\SDK\Library
	pip install ..\..\..\..\MEGA\MANUALS\DAC_ADC\AlazarTech\SDK\Library

	:: keysightSD1 (normal installation, files are in MEGA)
	ECHO Installing keysightSD1
	:: DR1 pip install ..\..\..\..\MEGAsync\MANUALS\DAC_ADC\KeySight\keysightSD1_3
	pip install ..\..\..\..\MEGA\MANUALS\DAC_ADC\KeySight\keysightSD1_3

	:: PYQUM (editable installation, files are in PYQUM)
	ECHO Installing PYQUM 101
	pip install -e .

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
