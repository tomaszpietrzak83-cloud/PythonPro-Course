@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."
set "PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe"
set "APP_DIR=%SCRIPT_DIR%room_booking"

if not exist "%PYTHON%" (
    echo Main course virtual environment was not found:
    echo %PYTHON%
    echo.
    echo From the repository root, create it with:
    echo python -m venv .venv
    exit /b 1
)

pushd "%APP_DIR%" || exit /b 1
"%PYTHON%" run.py
set "EXIT_CODE=%ERRORLEVEL%"
popd

exit /b %EXIT_CODE%
