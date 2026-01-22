
@echo off
setlocal
title RepoScan - Codebase Complexity Analyzer

echo ========================================================
echo   RepoScan: Codebase Depth & Complexity Analyzer
echo ========================================================
echo.
echo This tool will scan a folder and generate an Excel report 
echo containing file inventory and complexity metrics.
echo.

:ASK_DIR
set /p "TARGET_DIR=Enter the full path to the source code folder to scan: "

if "%TARGET_DIR%"=="" goto ASK_DIR
if not exist "%TARGET_DIR%" (
    echo.
    echo [ERROR] The folder "%TARGET_DIR%" does not exist.
    echo Please check the path and try again.
    echo.
    goto ASK_DIR
)

echo.
echo [1/2] Setting up environment...
cd repo_depth_analyser

echo [2/2] Running Analysis...
echo.
python main.py "%TARGET_DIR%" --output "../output_scan_results"

echo.
echo ========================================================
echo   Scan Complete!
echo ========================================================
echo.
echo Report saved to: output_scan_results folder
echo.
pause
