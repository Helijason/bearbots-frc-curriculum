@echo off
REM Copyright (c) 2026 BearBots FRC Team 6964
REM Open Source Software; you can modify and/or share it under the terms of
REM the MIT License available in the root directory of this project.
REM
REM Bear Bots replay launcher.
REM Double-click, or run  replay  from a terminal in this folder.
REM Passes any arguments through to replay.ps1 (e.g.  replay -List).
REM Uses the full path to powershell.exe in case it is not on PATH.
REM
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -ExecutionPolicy Bypass -File "%~dp0replay.ps1" %*
