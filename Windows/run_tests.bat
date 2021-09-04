@Echo Off

if [%1]==[] (
    goto :USAGE
)
if [%2]==[] (
    goto :USAGE
)

SET run_file=%1
SET tests_folder=%2

IF NOT EXIST %run_file% (
    ECHO %run_file% not found.
    goto :USAGE
)

IF NOT EXIST %tests_folder% (
    ECHO %tests_folder% not found. No tests directory.
    goto :USAGE
)

echo Running Tests..
for %%f in (%tests_folder%\*.in) do (
    IF EXIST "%tests_folder%\%%~nf.actual.out" (
        del "%tests_folder%\%%~nf.actual.out"
    )
	"%run_file%" < "%tests_folder%\%%~nf.in" > "%tests_folder%\%%~nf.actual.out"
)

ECHO ------------------------ RESULTS ------------------------
for %%f in (%tests_folder%\*.in) do (
    call fc "%tests_folder%\%%~nf.actual.out" "%tests_folder%\%%~nf.out" > nul 2> nul && (echo Test %%~nf : PASSED) || (echo Test %%~nf : FAILED)
)
goto :end


:USAGE
ECHO ------------------------ USAGE ------------------------
ECHO Usage: tst.bat my_prog.exe my_tests_folder
ECHO Written by Uriel
goto :end

:end
pause
