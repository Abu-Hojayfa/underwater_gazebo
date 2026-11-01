# RoboSub Underwater Environment Design Specification

## 1. System Architecture and Design Philosophy

The underwater competition environment is designed for **Gazebo Sim** (Harmonic / Garden / Fortress) using modular SDFormat (`.sdf`) 1.9/1.8 specifications. The environment prioritizes:
1. **Geometric and Physical Integrity:** Accurate dimensions reflecting official RoboSub rules, unambiguous collision boundaries, and avoidance of mesh penetration or surface artifacts.
2. **Modularity:** Reusable standalone model directories containing standard `model.sdf` and `model.config` files for each competition element.
3. **Perception-Ready Optics:** Tuned lighting, water attenuation backdrop, and high-contrast color markers optimized for autonomous computer vision pipelines (YOLO, OpenCV thresholding, and visual SLAM).
4. **Reproducibility:** A single authoritative configuration file (`config/environment.yaml`) and procedural generator (`scripts/generate_layout.py`) enabling parameterized course modifications without manual XML hacking.

---

## 2. Global Coordinate Frame and Reference Standards

The world coordinate frame follows the standard standard robotics coordinate convention (Right-Handed System, ENU):
- **Origin $(0, 0, 0)$:** Ground level at the center-left wall base of the pool start area ($X=0$ at start wall, $Y=0$ along course centerline, $Z=0$ at the pool floor).
- **$+X$ (Downrange Axis):** Forward along the longitudinal axis of the pool ($0.0\text{ m} \to 20.0\text{ m}$).
- **$+Y$ (Cross-Course Axis):** Lateral axis across pool width ($-5.0\text{ m}$ Port to $+5.0\text{ m}$ Starboard).
- **$+Z$ (Vertical Axis):** Directed upwards against gravity:
  - $z = 0.0\text{ m}$: Top surface of the pool floor slab.
  - $z = 4.0\text{ m}$: Nominal waterline (surface).
  - $z = 4.5\text{ m}$: Pool perimeter wall top edge ($0.5\text{ m}$ freeboard).

```
                      +Y (10m width)
           +5.0m ┌──────────────────────────────────────────────┐
                 │                                              │
                 │              [Target Board]                  │
                 │                 (X=14.2)                     │
   AUV Start     │     [Slalom Course]                          │
    (X=1.0)      │     (X=6.5 to 11.5)        [Octagon Zone]    │
  ----->         │ [Gate]                     (X=17.5, Y=0.0)   │ ---> +X (20m length)
   Y=0.0         │ (X=3.5)                     [Pinger/Table]   │
                 │                                              │
                 │     [Buoy Array]   [Bins]                    │
                 │       (X=12.8)     (X=14.0)                  │
                 │                                              │
           -5.0m └──────────────────────────────────────────────┘
                 0.0m                                         20.0m
```

---

## 3. Structural Pool Geometry

The pool model (`models/pool/model.sdf`) is implemented as a static entity (`<static>true</static>`) consisting of five distinct structural box segments:
1. **Floor Slab:** $20.0\text{ m} \times 10.0\text{ m} \times 0.3\text{ m}$, centered at $(10.0, 0.0, -0.15)$.
2. **Start Wall (West, $-X$):** $0.3\text{ m} \times 10.6\text{ m} \times 4.5\text{ m}$, centered at $(-0.15, 0.0, 2.25)$.
3. **End Wall (East, $+X$):** $0.3\text{ m} \times 10.6\text{ m} \times 4.5\text{ m}$, centered at $(20.15, 0.0, 2.25)$.
4. **South Wall (Port, $-Y$):** $20.0\text{ m} \times 0.3\text{ m} \times 4.5\text{ m}$, centered at $(10.0, -5.15, 2.25)$.
5. **North Wall (Starboard, $+Y$):** $20.0\text{ m} \times 0.3\text{ m} \times 4.5\text{ m}$, centered at $(10.0, 5.15, 2.25)$.

Each wall section includes full `<collision>` and `<visual>` geometries to prevent vehicle breach while offering zero penetration risk.

---

## 4. Optical and Lighting Environment

Underwater environments present specific visual characteristics: blue wavelength dominance, light absorption, and absence of harsh black shadows.
- **Ambient Illumination:** Cyan-tinted ambient light (`[0.35, 0.55, 0.65, 1.0]`) fills all shadow areas, simulating underwater ambient scatter.
- **Background Color:** Deep ocean cyan haze (`[0.05, 0.25, 0.35, 1.0]`) ensures distant visual horizons fade smoothly rather than displaying default skybox artifacts.
- **Directional Sunlight:** Oriented downwards from the water surface (`direction: [-0.3, 0.2, -0.9]`), providing realistic top-down illumination through the water column with diffuse value `[0.75, 0.88, 0.95, 1.0]`.

---

## 5. Gazebo System Plugins

The main world file (`worlds/robosub_pool.sdf`) incorporates standard Gazebo Sim core systems:
1. `gz-sim-physics-system`: Physics engine stepping and collision handling.
2. `gz-sim-user-commands-system`: Interactive user command management (spawning, moving, deleting models).
3. `gz-sim-scene-broadcaster-system`: Broadcasts rendering tree state to Gazebo GUI clients and headless sensor plugins.
4. `gz-sim-buoyancy-system`: Water density simulation ($\rho = 1000\text{ kg/m}^3$) with configured waterline at $z = 4.0\text{ m}$.

---

## 6. Procedural Regeneration Workflow

The entire environment layout can be procedurally recalculated using:
```bash
python scripts/generate_layout.py --config config/environment.yaml --output worlds/robosub_pool.sdf
```
This guarantees that changes to pool dimensions, object locations, or target colors remain synchronized across world files, models, and layout documentation.
