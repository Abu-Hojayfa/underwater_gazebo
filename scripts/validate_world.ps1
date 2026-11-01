<#
.SYNOPSIS
    RoboSub Gazebo Environment Static Validation Script (PowerShell)
#>
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RoboSub Gazebo Simulation Static Validation Suite (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Project Root: $ProjectRoot"
Write-Host "Running automated SDF and Model Reference test suite..." -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------"

Push-Location $ProjectRoot
try {
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -eq 0) {
        Write-Host "----------------------------------------------------------------------"
        Write-Host "[+] ALL VALIDATION CHECKS PASSED SUCCESSFULLY." -ForegroundColor Green
        exit 0
    } else {
        Write-Host "----------------------------------------------------------------------"
        Write-Host "[-] VALIDATION CHECKS FAILED." -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
