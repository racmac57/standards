@echo off
REM ============================================================================
REM Process Chatlog for unified_data_dictionary
REM ============================================================================
REM Version: 1.4.0 (Last-Mile: 5s archive buffer, xcopy /C access-denied recovery, absolute junction paths)
REM CLAUDE.md Compliance: MAX_PATH=260, RESERVED=100, MIN_FLOOR=10
REM ============================================================================

setlocal enabledelayedexpansion

REM Project paths - FORCE ABSOLUTE (junction-aware; only these targets for raw/chunked archive)
REM Directory Opus: pass absolute path e.g. "{filepath}" or "{allfilepath}" to avoid relative-path confusion.
set "RAW_DIR=C:\_chunker\docs\raw"
set "CHUNKED_DIR=C:\_chunker\docs\chunked"
set "CHUNKER_ROOT=C:\_chunker"

REM External paths
set "CHUNKER_INPUT=C:\_chunker\02_data"
set "CHUNKER_OUTPUT=C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

REM ============================================================================
REM PATH SAFETY CONSTANTS (CLAUDE.md compliance - must match watcher_splitter.py)
REM ============================================================================
set "MAX_PATH_LIMIT=260"
set "RESERVED_BUFFER=100"
set "MIN_TRUNCATION_FLOOR=10"

REM ============================================================================
REM CALCULATE MAX SUBFOLDER LENGTH
REM Formula: max_subfolder = MAX_PATH - len(CHUNKED_DIR) - RESERVED
REM ============================================================================
REM Get length of CHUNKED_DIR
set "TEMP_STR=%CHUNKED_DIR%"
set "CHUNKED_DIR_LEN=0"
:STRLEN_LOOP
if defined TEMP_STR (
    set "TEMP_STR=!TEMP_STR:~1!"
    set /a CHUNKED_DIR_LEN+=1
    goto STRLEN_LOOP
)

REM Calculate max subfolder length
set /a MAX_SUBFOLDER=%MAX_PATH_LIMIT% - %CHUNKED_DIR_LEN% - %RESERVED_BUFFER%

REM Apply minimum floor (CLAUDE.md requirement)
if !MAX_SUBFOLDER! LSS %MIN_TRUNCATION_FLOOR% (
    echo [WARNING] Path dangerously deep! MAX_SUBFOLDER=!MAX_SUBFOLDER! ^< %MIN_TRUNCATION_FLOOR%
    echo [WARNING] Setting to minimum floor of %MIN_TRUNCATION_FLOOR% characters
    set "MAX_SUBFOLDER=%MIN_TRUNCATION_FLOOR%"
)

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
echo  UNIFIED DATA DICTIONARY - CHATLOG PROCESSOR v1.4.0
echo ============================================================================
echo.
echo Processing: %FILENAME%
echo.
echo [PATH-SAFETY] CHUNKED_DIR length: !CHUNKED_DIR_LEN! chars
echo [PATH-SAFETY] Max subfolder name: !MAX_SUBFOLDER! chars (260 - !CHUNKED_DIR_LEN! - 100)

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
    echo   [OK] Saved to: docs\raw\%FILENAME%
)

REM ============================================================================
REM STEP 2: Send Atomic Copy to Chunker
REM ============================================================================
echo.
echo [STEP 2/4] Sending atomic copy to chunker...

REM Sync guard: allow OneDrive junction to settle before copy
timeout /t 3 /nobreak >nul
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
    if exist "01_scripts\Start_Chunker_Watcher.bat" (
        REM Use start /B to run without creating a visible window
        start "" /B /MIN cmd /c "01_scripts\Start_Chunker_Watcher.bat"
    ) else (
        echo   [WARNING] Start_Chunker_Watcher.bat not found at %CHUNKER_ROOT%\01_scripts
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
REM NOTE: Removed " and * substitutions - they corrupt batch variable expansion
set "SEARCH_BASENAME=!SEARCH_BASENAME:<=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:>=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME::=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:|=_!"
set "SEARCH_BASENAME=!SEARCH_BASENAME:?=_!"

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

REM Timeout buffer (5s): allow OneDrive to release sync locks on 04_output before archive
timeout /t 5 /nobreak >nul

REM ============================================================================
REM STEP 4: Copy Output to Project (OneDrive path-safety + access-denied recovery)
REM ============================================================================
echo.
echo [STEP 4/4] Retrieving chunked files...

if not exist "%CHUNKED_DIR%" mkdir "%CHUNKED_DIR%"

REM ============================================================================
REM DEST_SUB EXTRACTION AND PATH-SAFE TRUNCATION (CLAUDE.md compliance)
REM ============================================================================

REM Extract the folder name from FOUND_PATH (last segment after backslash)
for %%F in ("!FOUND_PATH!") do set "DEST_SUB=%%~nxF"

echo   [PATH-SAFETY] Source folder: !DEST_SUB!

REM ABBREVIATION PARITY: Apply udd and Std substitutions (must match watcher_splitter.py)
set "DEST_SUB_SAFE=!DEST_SUB!"
set "DEST_SUB_SAFE=!DEST_SUB_SAFE:unified_data_dictionary=udd!"
set "DEST_SUB_SAFE=!DEST_SUB_SAFE:Standards=Std!"

REM Check if abbreviations were applied
if not "!DEST_SUB_SAFE!"=="!DEST_SUB!" (
    echo   [PATH-SAFETY] Abbreviations applied: '!DEST_SUB!' -^> '!DEST_SUB_SAFE!'
)

REM Get length of DEST_SUB_SAFE
set "TEMP_STR=!DEST_SUB_SAFE!"
set "DEST_SUB_LEN=0"
:DEST_STRLEN_LOOP
if defined TEMP_STR (
    set "TEMP_STR=!TEMP_STR:~1!"
    set /a DEST_SUB_LEN+=1
    goto DEST_STRLEN_LOOP
)

REM DYNAMIC TRUNCATION: Truncate if exceeds MAX_SUBFOLDER
set "TRUNCATED=0"
if !DEST_SUB_LEN! GTR !MAX_SUBFOLDER! (
    set "TRUNCATED=1"
    set "ORIGINAL_LEN=!DEST_SUB_LEN!"
    REM Truncate to MAX_SUBFOLDER length
    set "DEST_SUB_SAFE=!DEST_SUB_SAFE:~0,%MAX_SUBFOLDER%!"
    echo   [PATH-SAFETY] Truncated: !ORIGINAL_LEN! -^> !MAX_SUBFOLDER! chars
)

REM Final destination path
set "DEST_FULL=%CHUNKED_DIR%\!DEST_SUB_SAFE!"

echo   [PATH-SAFETY] Destination: !DEST_SUB_SAFE!

REM Verify final path length
set "TEMP_STR=!DEST_FULL!"
set "DEST_FULL_LEN=0"
:DESTFULL_STRLEN_LOOP
if defined TEMP_STR (
    set "TEMP_STR=!TEMP_STR:~1!"
    set /a DEST_FULL_LEN+=1
    goto DESTFULL_STRLEN_LOOP
)

echo   [PATH-SAFETY] Final path length: !DEST_FULL_LEN! chars (limit: %MAX_PATH_LIMIT%)
if !DEST_FULL_LEN! GTR %MAX_PATH_LIMIT% (
    echo   [ERROR] Path still exceeds limit after truncation!
    echo   [ERROR] Please shorten project path or reduce filename length.
    pause
    exit /b 1
)

REM 5s buffer before archive: OneDrive may still be locking 04_output files for upload
timeout /t 5 /nobreak >nul
REM xcopy /C: continue on "Access Denied" / "File in Use" so batch survives locked files
xcopy "!FOUND_PATH!" "!DEST_FULL!\" /E /I /Y /C >nul
set "COPY_RESULT=!ERRORLEVEL!"

if !COPY_RESULT! EQU 0 (
    echo   [OK] Copied data to: docs\chunked\!DEST_SUB_SAFE!\
) else (
    echo   [WARNING] Copy may have issues - errorlevel: !COPY_RESULT!
    echo   Please verify: !DEST_FULL!
)

echo.
echo ============================================================================
echo  PROCESSING COMPLETE
echo ============================================================================
echo.
echo Raw Source:  docs\raw\%FILENAME%
echo Processed:   docs\chunked\!DEST_SUB_SAFE!\
if !TRUNCATED! EQU 1 (
    echo [PATH-SAFETY] Folder name was truncated to fit OneDrive path limits.
)
echo.
echo ============================================================================

timeout /t 4 /nobreak >nul
exit /b 0
