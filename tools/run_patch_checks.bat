@echo off
setlocal
if "%~1"=="" (
  echo Usage: tools\run_patch_checks.bat PATCH_NUMBER
  echo Example: tools\run_patch_checks.bat 36_1
  exit /b 2
)
python tools\run_patch_checks.py %1
if errorlevel 1 (
  py tools\run_patch_checks.py %1
)
