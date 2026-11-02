<#
.SYNOPSIS
    RoboSub Competition Simulation Environment Launch Script (PowerShell / Windows)
.DESCRIPTION
    Dynamically resolves project root, validates environment prerequisites,
    configures Gazebo model resource paths, and launches Gazebo Sim.
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$GzArgs
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path "$ScriptDir\..").Path
$WorldFile = Join-Path $ProjectRoot "worlds\robosub_pool.sdf"
$ModelsDir = Join-Path $ProjectRoot "models"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RoboSub Underwater Competition Gazebo Simulation Launcher (Windows)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Project Root: $ProjectRoot"
Write-Host "World File:   $WorldFile"
Write-Host "Models Dir:   $ModelsDir"
Write-Host "----------------------------------------------------------------------"

# 1. Verify World File
if (-not (Test-Path $WorldFile)) {
    Write-Error "[-] World file not found at $WorldFile. Run 'python scripts/generate_layout.py' first."
    exit 1
}

# 2. Check Gazebo Sim Binary
$GzBinary = Get-Command "gz" -ErrorAction SilentlyContinue
$IgnBinary = Get-Command "ign" -ErrorAction SilentlyContinue

if ($GzBinary) {
    $LaunchCmd = "gz"
    $SubCmd = "sim"
} elseif ($IgnBinary) {
    $LaunchCmd = "ign"
    $SubCmd = "gazebo"
} else {
    Write-Host "[-] Note: Neither 'gz' nor 'ign' binary was found in PATH." -ForegroundColor Yellow
    Write-Host "    Modern Gazebo Sim is typically executed within WSL2 (Ubuntu 24.04/22.04) or native Linux." -ForegroundColor Yellow
    Write-Host "    If running in WSL2, execute: ./scripts/launch_world.sh" -ForegroundColor Yellow
    Write-Host "----------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "[+] Fallback: Starting Real-Time 3D Web Simulator (Three.js + Cannon.js)..." -ForegroundColor Green
    & "$ScriptDir\launch_web_sim.ps1"
    exit 0
}

# 3. Configure Resource Paths
$env:GZ_SIM_RESOURCE_PATH = "$ModelsDir;" + $env:GZ_SIM_RESOURCE_PATH
$env:IGN_GAZEBO_RESOURCE_PATH = "$ModelsDir;" + $env:IGN_GAZEBO_RESOURCE_PATH
$env:SDF_PATH = "$ModelsDir;" + $env:SDF_PATH

Write-Host "[+] Configured GZ_SIM_RESOURCE_PATH: $env:GZ_SIM_RESOURCE_PATH" -ForegroundColor Green
Write-Host "[+] Launching: $LaunchCmd $SubCmd -r $WorldFile $GzArgs" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

& $LaunchCmd $SubCmd -r $WorldFile @GzArgs
