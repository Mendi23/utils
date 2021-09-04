@Echo Off
REM this is acomment

:: change name of all file in a folder...
for /d %%d in (*) do (
		ECHO %%d
if exist "%%d"\*.mp4 REN "%%d"\*.mp4 "MY Show %%d.mp4"
MOVE "%%d"\*.mp4 ./
)

pause
