# replay.ps1 — Bear Bots AdvantageKit replay helper
#
# What it does:
#   1. Finds the newest recorded log in .\logs (ignores _sim replay outputs)
#   2. Sets AKIT_LOG_PATH so build.gradle disables sim extensions and the
#      robot code loads that exact log
#   3. Runs replayWatch
#
# Usage:
#   .\replay.ps1                 -> replay the newest log
#   .\replay.ps1 mylog.wpilog    -> replay a specific log in .\logs
#   .\replay.ps1 -List           -> just list available logs and exit
#
# Before running: set simMode = REPLAY in Constants.java.
# Have AdvantageScope open to watch results update live.

param(
    [string]$LogName = "",
    [switch]$List
)

$logsDir = Join-Path $PSScriptRoot "logs"

# --- sanity: logs folder exists ---
if (-not (Test-Path $logsDir)) {
    Write-Host "No 'logs' folder found here." -ForegroundColor Red
    Write-Host "Run the robot in SIM mode first to record a log, then try again." -ForegroundColor Yellow
    exit 1
}

# --- gather original logs only (exclude _sim replay outputs) ---
$logs = Get-ChildItem -Path $logsDir -Filter *.wpilog |
        Where-Object { $_.Name -notlike "*_sim.wpilog" } |
        Sort-Object LastWriteTime -Descending

if ($logs.Count -eq 0) {
    Write-Host "No recorded logs found in 'logs'." -ForegroundColor Red
    Write-Host "Run the robot in SIM mode first to record one." -ForegroundColor Yellow
    exit 1
}

# --- list mode: show logs and quit ---
if ($List) {
    Write-Host "Available logs (newest first):" -ForegroundColor Cyan
    $i = 1
    foreach ($l in $logs) {
        Write-Host ("  {0}. {1}  ({2})" -f $i, $l.Name, $l.LastWriteTime)
        $i++
    }
    exit 0
}

# --- choose the log ---
if ($LogName -ne "") {
    $chosen = $logs | Where-Object { $_.Name -eq $LogName } | Select-Object -First 1
    if ($null -eq $chosen) {
        Write-Host "No log named '$LogName' in 'logs'." -ForegroundColor Red
        Write-Host "Run  .\replay.ps1 -List  to see what's available." -ForegroundColor Yellow
        exit 1
    }
} else {
    $chosen = $logs[0]
}

# --- set the env var and run ---
$env:AKIT_LOG_PATH = $chosen.FullName

Write-Host ""
Write-Host "Replaying: $($chosen.Name)" -ForegroundColor Green
Write-Host "Make sure simMode = REPLAY in Constants.java." -ForegroundColor Yellow
Write-Host "Open AdvantageScope to watch results update as you edit code." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

$env:HALSIM_EXTENSIONS = ""
$env:AKIT_LOG_PATH = $chosen.FullName

.\gradlew replayWatch
