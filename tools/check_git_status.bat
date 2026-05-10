@echo off
setlocal

echo ALETHEIA Git status helper

git --version >nul 2>&1
if errorlevel 1 (
  echo Git is not installed or not available on PATH.
  echo Continue using patched-items-only zip workflow.
  exit /b 1
)

if not exist .git (
  echo This folder is not a Git repository yet.
  echo To initialize:
  echo   git init
  echo   git add .
  echo   git commit -m "ALETHEIA baseline"
  exit /b 2
)

git status --short
if errorlevel 1 exit /b 1

echo.
echo To export local changes:
echo   tools\export_patch_diff.bat PATCH_local_changes.diff
