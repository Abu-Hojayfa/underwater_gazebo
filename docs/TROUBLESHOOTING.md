# RoboSub Gazebo Simulation Troubleshooting Guide

This guide details common setup, resource path, rendering, physics, and execution issues encountered when deploying the RoboSub simulation environment in Gazebo Sim.

---

## 1. Missing Gazebo Binaries (`gz: command not found`)

### Symptom
Executing `scripts/launch_world.sh` or `scripts/launch_world.ps1` returns:
```
[-] Error: Neither 'gz' nor 'ign' binary was found in PATH.
```

### Cause
Gazebo Sim (formerly Ignition Gazebo) is not installed on the current host or is not present in the system environment `$PATH`.

### Solution
Install **Gazebo Harmonic** (recommended) on Ubuntu 24.04 (Noble) or Ubuntu 22.04 (Jammy) via the official Open Robotics package repository:

```bash
# 1. Install prerequisites
sudo apt-get update && sudo apt-get install -y lsb-release wget gnupg

# 2. Add Open Robotics GPG key and repository
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# 3. Install Gazebo Harmonic
sudo apt-get update && sudo apt-get install -y gz-harmonic
```

For Windows users without native Gazebo, install WSL2 and execute the commands inside Ubuntu:
```powershell
wsl --install -d Ubuntu-24.04
```

---

## 2. Resource Path Errors (`Unable to find uri[model://...]`)

### Symptom
When launching `robosub_pool.sdf`, Gazebo outputs error messages such as:
```
[Err] [Server.cc:...] Unable to find uri[model://pool]
[Err] [Server.cc:...] Unable to find uri[model://gate]
```
The simulation loads as an empty or partially populated world without competition objects.

### Cause
Gazebo Sim resolves `model://` URIs using the `GZ_SIM_RESOURCE_PATH` (or legacy `IGN_GAZEBO_RESOURCE_PATH` and `SDF_PATH`) environment variable. If these variables do not include the absolute path to this repository's `models/` directory, model lookups fail.

### Solution
Always launch the environment using the provided launcher scripts:
```bash
./scripts/launch_world.sh
```
Or manually export the variable in your current terminal:
```bash
export GZ_SIM_RESOURCE_PATH="/path/to/underwater_gazebo/models:${GZ_SIM_RESOURCE_PATH}"
export SDF_PATH="/path/to/underwater_gazebo/models:${SDF_PATH}"
gz sim -r worlds/robosub_pool.sdf
```

---

## 3. Headless Server and OpenGL Rendering Failures

### Symptom
Launching the simulation on a remote server, CI/CD runner, or headless container results in:
```
libGL error: MESA-LOADER: failed to open swrast
[GUI] [Err] [Ogre2RenderEngine.cc:...] Failed to create OpenGL context
```

### Cause
Gazebo Sim GUI requires hardware 3D acceleration or a software OpenGL rasterizer with an active X11/Wayland display server.

### Solution
1. **Run Headless (Server Mode):**
   If only physics, sensor plugins, or ROS 2 bridges are needed, launch Gazebo without the GUI (`-s` flag):
   ```bash
   gz sim -s -r worlds/robosub_pool.sdf
   ```
2. **Enable Mesa Software Rasterization:**
   ```bash
   export LIBGL_ALWAYS_SOFTWARE=1
   export MESA_GL_VERSION_OVERRIDE=3.3
   ```
3. **Virtual Framebuffer (Xvfb):**
   For automated rendering tests in CI:
   ```bash
   xvfb-run -s "-screen 0 1920x1080x24" gz sim -r worlds/robosub_pool.sdf
   ```

---

## 4. SDFormat Version Compatibility Warnings

### Symptom
Gazebo Sim logs warning messages regarding SDF version:
```
[Wrn] [Root.cc:...] Version 1.9 is newer than the supported version 1.8
```

### Cause
The environment uses SDFormat 1.9 by default. If running an older Gazebo release (such as Gazebo Fortress / gz-sim 6), the engine may default to SDFormat 1.8.

### Solution
The models and world file use standard geometric primitives and standard tags compatible across SDFormat 1.8, 1.9, and 1.10. To target version 1.8 explicitly, run the layout generator with your desired version:
```bash
python3 scripts/generate_layout.py
```
Or replace `<sdf version="1.9">` with `<sdf version="1.8">` across `worlds/robosub_pool.sdf` and `models/*/model.sdf`.

---

## 5. Vehicle Buoyancy and Physics Instability

### Symptom
The generic AUV placeholder falls directly to the floor or accelerates violently toward the surface.

### Cause
Gazebo Sim's `gz-sim-buoyancy-system` calculates net buoyant force as:
$$F_{\text{buoyancy}} = \rho_{\text{fluid}} \cdot V_{\text{displaced}} \cdot g$$
If vehicle collision geometry volume does not match vehicle mass ($\approx 25\text{ kg}$), the vehicle will experience net positive or negative buoyancy.

### Solution
1. In `models/auv_placeholder/model.sdf`, adjust the vehicle mass under `<inertial><mass>` to match total displaced volume ($\approx 0.025\text{ m}^3$ for neutral buoyancy in $1000\text{ kg/m}^3$ freshwater).
2. Ensure the `<uniform_fluid_density>1000.0</uniform_fluid_density>` parameter is active inside the world buoyancy plugin.
3. For static positioning tests without physics dynamics, set `<static>true</static>` inside `models/auv_placeholder/model.sdf`.

---

## 6. Visual Geometry vs. Functional Manipulation

### Important Distinction
- **Path Markers and Octagon Lines:** Designed as visual-only entities without rigid collision geometry to avoid snagging vehicle skids or thrusters.
- **Bins and Target Board:** Feature accurate rigid collision geometry on frame walls and stands.
- **Acoustic Pinger & Mission Objects:** Represent high-fidelity visual and spatial placeholders for robotics navigation algorithms. Interfacing with acoustic sensors or marker drop payloads requires corresponding ROS 2 sensor/actuator bridge plugins.
