<#
.SYNOPSIS
    RoboSub Real-Time Web Simulator Launcher (PowerShell)
#>
$Port = 8080
$Url = "http://localhost:$Port/web_simulator.html"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RoboSub Real-Time Web Simulator (Physics + Controllable AUV)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Starting local lightweight server at $Url ..." -ForegroundColor Green
Write-Host "Press Ctrl+C in this terminal to stop the server when done." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray

Start-Process $Url
python -m http.server $Port

