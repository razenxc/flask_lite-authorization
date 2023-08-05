@echo off
REM
if "%~1"=="" (
    echo "Enter launch options------------------"
    echo " --dev ; for run development flask server"
    echo " --prod ; for run production waitress server"
    echo " --host <ip> ; for change server ip (default localhost/127.0.0.1)"
    echo "--------------------------------------"
) else if "%~1"=="--dev" (
    REM
    if "%~2"=="" (
        flask --app liteauth:app run --debug
    ) else (
        flask --app liteauth:app run --debug --host %~2
    )
) else if "%~1"=="--prod" (
    REM
    if "%~2"=="" (
        waitress-serve --host localhost --call liteauth:app
    ) else (
        waitress-serve --host %~2 --call liteauth:app
    )
) else (
    echo Invalid parameter: %~1
)
