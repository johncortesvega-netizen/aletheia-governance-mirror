@echo off
setlocal

if "%~1"=="" (
  echo Usage: tools\export_patch_diff.bat ^<output.diff^>
  exit /b 2
)

git --version >nul 2>&1
if errorlevel 1 (
  echo Git is not installed or not available on PATH.
  exit /b 1
)

if not exist .git (
  echo This folder is not a Git repository yet.
  echo Run git init / git add . / git commit before using diff export.
  exit /b 2
)

git diff --binary -- . > "%~1"
if errorlevel 1 exit /b 1

echo Wrote %~1
