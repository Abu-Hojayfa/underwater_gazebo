#!/usr/bin/env bash
# ==============================================================================
# RoboSub Gazebo Environment Static Validation Script (Bash)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "======================================================================"
echo "  RoboSub Gazebo Simulation Static Validation Suite"
echo "======================================================================"
echo "Project Root: ${PROJECT_ROOT}"
echo "Running automated SDF and Model Reference test suite..."
echo "----------------------------------------------------------------------"

cd "${PROJECT_ROOT}"

# Run Python unit tests
if python3 -m unittest discover -s tests -v; then
    echo "----------------------------------------------------------------------"
    echo "[+] ALL VALIDATION CHECKS PASSED SUCCESSFULLY."
    exit 0
else
    echo "----------------------------------------------------------------------"
    echo "[-] VALIDATION CHECKS FAILED."
    exit 1
fi
