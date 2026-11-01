@echo off
echo ======================================================================
echo   RoboSub Real-Time Web Simulator Launcher
echo ======================================================================
echo Starting local web server on http://localhost:8080 ...
echo Opening web simulator in your default browser...
start http://localhost:8080/web_simulator.html
python -m http.server 8080

