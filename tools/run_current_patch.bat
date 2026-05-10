@echo off
setlocal
if "%~1"=="" (
  echo Usage: tools\run_current_patch.bat PATCH_NUMBER
  echo Example: tools\run_current_patch.bat 36_1
  exit /b 2
)
call tools\run_patch_checks.bat %1
