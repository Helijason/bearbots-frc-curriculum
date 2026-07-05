@echo off
REM Bear Bots replay launcher.
REM Double-click, or run  replay  from a terminal in this folder.
REM Passes any arguments through to replay.ps1 (e.g.  replay -List).
REM Uses the full path to powershell.exe in case it is not on PATH.
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -ExecutionPolicy Bypass -File "%~dp0replay.ps1" %*
