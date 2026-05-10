@echo off
setlocal

echo Running ALETHEIA current safe checks...
echo.

echo [1/2] Running latest patch-specific safe check...
python tools\run_current_suite.py
if errorlevel 1 (
  py tools\run_current_suite.py
  if errorlevel 1 exit /b 1
)

echo.
echo [2/2] Reporting legacy test inventory ^(non-blocking^)...
python tools\run_legacy_test_inventory.py
if errorlevel 1 (
  py tools\run_legacy_test_inventory.py
)

echo.
echo ALETHEIA current safe checks passed.
echo Older historical patch contracts and legacy tests are documented separately and are not run by default.
