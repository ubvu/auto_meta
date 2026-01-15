::&commat;echo off
:: Check if UV is installed
if exist "C:\Users\%USERNAME%\.local\bin\uv.exe" GOTO :CreateVenv
:: If not then install it
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
:: Add the path to PATH
:: First check if it is run in cmd or powershell to provide the right command
:: Powershell automatically adds user-specific path in PSModulePath upon starting
echo %PSModulePath% | findstr /L %USERPROFILE% >NUL
IF %ERRORLEVEL% EQU 0 goto :ISPOWERSHELL

echo Not running from Powershell
SET Path=C:\Users\%USERNAME%\.local\bin;%Path%

GOTO :CreateVenv

:ISPOWERSHELL
$env:Path = "C:\Users\%USERNAME%\.local\bin;$env:Path"
:: Now invoke it to create a venv
:CreateVenv
uv venv --python 3.11.6
:: Activate the venv
CALL .venv/scripts/activate
:: Initialise project (create toml, etc), needed to create this template
uv init
:: Make the venv install everything from requirements.txt
uv add -r requirements.txt
pre-commit install
python get_spec.py
:: Patch to make sure pip is installed in the venv
python -m ensurepip --default-pip
:: Deactivate venv to ensure pip install and reactivate
deactivate
CALL .venv/scripts/activate
PAUSE
