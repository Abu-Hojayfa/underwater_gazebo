#!/usr/bin/env bash
# ==============================================================================
# RoboSub Competition Simulation Environment Launch Script (Bash / Linux / WSL)
# ==============================================================================
set -e

# Resolve script and project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

WORLD_FILE="${PROJECT_ROOT}/worlds/robosub_pool.sdf"
MODELS_DIR="${PROJECT_ROOT}/models"

echo "======================================================================"
echo "  RoboSub Underwater Competition Gazebo Simulation Launcher"
echo "======================================================================"
echo "Project Root: ${PROJECT_ROOT}"
echo "World File:   ${WORLD_FILE}"
echo "Models Dir:   ${MODELS_DIR}"
echo "----------------------------------------------------------------------"

# 1. Verify World File Existence
if [ ! -f "${WORLD_FILE}" ]; then
    echo "[-] Error: World file not found at ${WORLD_FILE}" >&2
    echo "    Run 'python3 scripts/generate_layout.py' to generate the environment." >&2
    exit 1
fi

# 2. Check for Gazebo Sim Binaries
GZ_CMD=""
if command -v gz &> /dev/null; then
    GZ_CMD="gz sim"
elif command -v ign &> /dev/null; then
    GZ_CMD="ign gazebo"
else
    echo "[-] Error: Neither 'gz' (Gazebo Harmonic/Garden) nor 'ign' (Gazebo Fortress) executable was found in PATH." >&2
    echo "    To install Gazebo Harmonic on Ubuntu 24.04 / 22.04 / WSL2:" >&2
    echo "      sudo apt-get update && sudo apt-get install -y gz-harmonic" >&2
    echo "    See docs/TROUBLESHOOTING.md for detailed installation instructions." >&2
    exit 2
fi

# 3. Configure Model Resource Environment Variables
export GZ_SIM_RESOURCE_PATH="${MODELS_DIR}:${GZ_SIM_RESOURCE_PATH}"
export IGN_GAZEBO_RESOURCE_PATH="${MODELS_DIR}:${IGN_GAZEBO_RESOURCE_PATH}"
export SDF_PATH="${MODELS_DIR}:${SDF_PATH}"

echo "[+] Configured GZ_SIM_RESOURCE_PATH=${GZ_SIM_RESOURCE_PATH}"
echo "[+] Launching: ${GZ_CMD} -r ${WORLD_FILE}"
echo "======================================================================"

# 4. Launch Gazebo Sim with optional extra arguments forwarded
exec ${GZ_CMD} -r "${WORLD_FILE}" "$@"
