@echo off
setlocal

echo Running ALETHEIA full pytest collection.
echo WARNING: legacy tests may currently fail until cleanup is complete.
echo.

python -m pytest -q tests --ignore=tests\tests
if errorlevel 1 (
  py -m pytest -q tests --ignore=tests\tests
  if errorlevel 1 exit /b 1
)

echo.
echo Full pytest collection passed.
