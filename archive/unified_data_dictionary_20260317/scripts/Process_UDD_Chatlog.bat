@echo off
REM ============================================================================
REM Process Chatlog for unified_data_dictionary
REM ============================================================================
REM Version: 1.1.0 (Enhanced: PID file-based watcher detection with fallback)
REM ============================================================================

setlocal enabledelayedexpansion

REM Project paths
set "PROJECT_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
set "RAW_DIR=%PROJECT_ROOT%\docs\chatlogs\raw"
set "CHUNKED_DIR=%PROJECT_ROOT%\docs\chatlogs\chunked"
set "CHUNKER_ROOT=C:\_chunker\opus"

REM External paths
set "CHUNKER_INPUT=C:\_chunker\02_data"
set "CHUNKER_OUTPUT=C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

REM ============================================================================
REM CHECK: File Selection
REM ============================================================================
if "%~1"=="" (
    echo [ERROR] No file selected.
    pause
    exit /b 1
)

set "INPUT_FILE=%~1"
set "FILENAME=%~nx1"
set "BASENAME=%~n1"

echo.
echo ============================================================================
echo  UNIFIED DATA DICTIONARY - CHATLOG PROCESSOR v1.1.0
echo ============================================================================
echo.
echo Processing: %FILENAME%

REM ============================================================================
REM STEP 1: Move to Project Raw Folder
REM ============================================================================
echo [STEP 1/4] Saving to project raw folder...

if not exist "%RAW_DIR%" mkdir "%RAW_DIR%"

if /i "%~dp1"=="%RAW_DIR%\" (
    echo   [INFO] File is already in raw folder.
) else (
    move /Y "%INPUT_FILE%" "%RAW_DIR%\" >nul
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to move to raw folder.
        pause
        exit /b 1
    )
    echo   [OK] Saved to: docs\chatlogs\raw\%FILENAME%
)

REM ============================================================================
REM STEP 2: Send Atomic Copy to Chunker
REM ============================================================================
echo.
echo [STEP 2/4] Sending atomic copy to chunker...

REM 1. Copy as .part (Watcher ignores this)
copy /Y "%RAW_DIR%\%FILENAME%" "%CHUNKER_INPUT%\%FILENAME%.part" >nul

REM 2. Rename to final .md (Watcher sees ONE event)
ren "%CHUNKER_INPUT%\%FILENAME%.part" "%FILENAME%"

REM ============================================================================
REM Check if watcher is already running (enhanced with PID file support)
REM Detection priority:
REM   1. PID file (C:\_chunker\watcher_pid.txt) - most precise
REM   2. General Python process check - fallback
REM ============================================================================
echo   Checking watcher status...

set "WATCHER_RUNNING=0"
set "WATCHER_PID="
set "PID_FILE=C:\_chunker\watcher_pid.txt"

REM Try PID file detection first (more precise)
if exist "!PID_FILE!" (
    REM Read PID from file
    for /f "usebackq tokens=* delims=" %%p in ("!PID_FILE!") do (
        set "WATCHER_PID=%%p"
    )

    REM Verify we got a PID and it's a running Python process
    if defined WATCHER_PID (
        tasklist /FI "PID eq !WATCHER_PID!" 2>nul | find /I "python" >nul
        if !ERRORLEVEL! EQU 0 (
            set "WATCHER_RUNNING=1"
            echo   [INFO] Watcher running via PID file ^(PID: !WATCHER_PID!^)
        ) else (
            echo   [INFO] PID file exists but process !WATCHER_PID! not found
        )
    ) else (
        echo   [INFO] PID file exists but is empty
    )
)

REM Fallback to general Python process check if PID detection failed
if !WATCHER_RUNNING! EQU 0 (
    tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
    if !ERRORLEVEL! EQU 0 (
        set "WATCHER_RUNNING=1"
        echo   [INFO] Watcher process detected ^(general Python check^)
    )
)

REM Start watcher if not running
if !WATCHER_RUNNING! EQU 0 (
    echo   Starting Watcher...
    pushd "%CHUNKER_ROOT%"
    if exist "Start_Chunker_Watcher.bat" (
        REM Use start /B to run without creating a visible window
        start "" /B /MIN cmd /c "Start_Chunker_Watcher.bat"
    ) else (
        echo   [WARNING] Start_Chunker_Watcher.bat not found at %CHUNKER_ROOT%
    )
    popd
    timeout /t 3 /nobreak >nul
)

echo   [OK] File queued for processing

REM ============================================================================
REM STEP 3: Monitor for Output
REM ============================================================================
echo.
echo [STEP 3/4] Waiting for processed files...
echo   Target: %BASENAME%...

set "TIMEOUT_COUNT=0"
set "FOUND_PATH="

REM ============================================================================
REM Build sanitized search pattern (matches watcher_splitter.py logic)
REM watcher_splitter.py does:
REM   1. Replace spaces with underscores
REM   2. Replace invalid chars <>:"|?* with underscores
REM   3. Truncate to 60 characters
REM ============================================================================
set "SEARCH_BASENAME=%BASENAME%"

REM Replace spaces with underscores
set "SEARCH_BASENAME=!SEARCH_BASENAME: =_!"

REM Replace special characters that sanitize_folder_name() handles
set "SEARCH_BASENAME=!SEARCH_BASENAME:<=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:>=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME::=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:"=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:|=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:?=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:*=_!"

REM Handle truncation - only use first 60 characters for search
REM (Batch substring: !var:~start,length!)
set "SEARCH_BASENAME=!SEARCH_BASENAME:~0,60!"

:WAIT_FOR_CHUNK
timeout /t 2 /nobreak >nul
set /a TIMEOUT_COUNT+=2

REM Debug ticker every 10 seconds
set /a MOD_CHECK=!TIMEOUT_COUNT! %% 10
if !MOD_CHECK! EQU 0 echo   ...scanning (!TIMEOUT_COUNT!s elapsed)

REM Look for a DIRECTORY matching the sanitized basename
for /d %%D in ("%CHUNKER_OUTPUT%\!SEARCH_BASENAME!*") do (
    set "FOUND_PATH=%%D"
    goto FILES_FOUND
)

REM Wait max 120 seconds (extended for OneDrive sync delays)
if !TIMEOUT_COUNT! LSS 120 goto WAIT_FOR_CHUNK

echo.
echo [ERROR] Chunking Timed Out after !TIMEOUT_COUNT! seconds
echo.
echo Diagnostics:
echo   Input file: %CHUNKER_INPUT%\%FILENAME%
if exist "%CHUNKER_INPUT%\%FILENAME%" (
    echo   [STATUS] File still in input directory - watcher may not be running
) else (
    echo   [STATUS] File removed from input - may be processing or in archive
)
echo.
echo   Output directory: %CHUNKER_OUTPUT%
echo   Searching for: !SEARCH_BASENAME!*
echo.
echo Troubleshooting:
echo   1. Check if watcher is running (Task Manager - python.exe)
echo   2. Check logs: C:\_chunker\05_logs\
echo   3. Check archive: C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\03_archive
echo.
pause
exit /b 1

:FILES_FOUND
echo   [OK] Found output: %FOUND_PATH%

REM Allow OneDrive a moment to sync
timeout /t 2 /nobreak >nul

REM ============================================================================
REM STEP 4: Copy Output to Project
REM ============================================================================
echo.
echo [STEP 4/4] Retrieving chunked files...

if not exist "%CHUNKED_DIR%" mkdir "%CHUNKED_DIR%"

REM Copy the results back to the project
xcopy "%FOUND_PATH%" "%CHUNKED_DIR%\" /E /I /Y >nul
set "COPY_RESULT=%ERRORLEVEL%"

if %COPY_RESULT% EQU 0 (
    echo   [OK] Copied data to: docs\chatlogs\chunked\
) else (
    echo   [WARNING] Copy may have issues - errorlevel: %COPY_RESULT%
    echo   Please verify: %CHUNKED_DIR%
)

echo.
echo ============================================================================
echo  PROCESSING COMPLETE
echo ============================================================================
echo.
echo Raw Source:  docs\chatlogs\raw\%FILENAME%
echo Processed:   docs\chatlogs\chunked\
echo.
echo ============================================================================

timeout /t 4 /nobreak >nul
exit /b 0
