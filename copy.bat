
@echo off

echo "============================================================================"
echo "|                              mybackup v0.01                              |"
echo "|==========================================================================|"
echo "|                            1) copy and archive                           |"
echo "|                            2) only copy                                  |"
echo "|                            3) only archive                               |"
echo "|                            4) quit                                       |"
echo "============================================================================"


set /p ch="please choice a num:"

set DEST=E:\update
set SOUR=%~dp0

set dt=%date:~0,4%%date:~5,2%%date:~8,2%
set sd=%date:~5,2%-%date:~8,2%-%date:~0,4%

for /f "delims=" %%i in ("%SOUR:~0,-1%") do (set SOUR_DIR=%%~ni)

set dest_src_dir=%DEST%\%SOUR_DIR%\%dt%\src
set dest_arch_dir=%DEST%\%SOUR_DIR%\%dt%\arch

if not exist "%dest_src_dir%" (
	md "%dest_src_dir%"
)

if not exist "%dest_arch_dir%" (
	md "%dest_arch_dir%"
)


if %ch% == 1 ( call :ca )else ( 
	if %ch% == 2 ( call :c )else (
			if %ch% == 3 ( call :a )else (
					call :q
				)
		)
	)


call :end
goto :eof

:ca
call :c
call :a
goto :eof


:q
exit
goto :eof

:c

set /p in_sd="please input a day:"

if not "%in_sd%" == "" (
	set sd=%in_sd%
)

xcopy %SOUR:~0,-1% %dest_src_dir% /d:%sd% /s

del %dest_src_dir%\%~n0.bat

goto :eof

:a
%dest_arch_dir:~0,2%

cd %dest_arch_dir%

rar a %dest_arch_dir%\%SOUR_DIR%_%dt%%time:~0,2%%time:~3,2%%time:~6,2%.rar ../src

goto :eof

:end
pause