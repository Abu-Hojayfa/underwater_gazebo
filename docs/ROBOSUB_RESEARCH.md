# RoboSub Underwater Competition Environment Research

## Overview and Metadata
- **Research Date:** November 2026
- **Target Competition Ruleset:** RoboSub Autonomy Challenge (Handbook Years 2024–2026, Theme: *Storm Response* and Core Autonomy Specifications), supplemented by RoboSub International Student Competition Historical Specifications (RoboNation).
- **Target Simulation Engine:** Gazebo Sim (Harmonic / Garden / Fortress compatible SDFormat 1.9/1.8).
- **Coordinate Convention:** Right-handed Cartesian coordinates:
  - **+X:** Main course forward navigation axis (downrange from start dock/gate towards octagon).
  - **+Y:** Pool lateral axis (port / starboard relative to start heading).
  - **+Z:** Vertical axis (+Z upwards, water surface at pool waterline, pool floor at $z = 0.0\text{ m}$).

---

## 1. Primary Sources and Reference Materials

1. **RoboSub Official Website & RoboNation Portal**
   - URL: [https://robosub.org/](https://robosub.org/)
   - Key Information: Annual competition overview, event schedules, mission themes.

2. **RoboSub Team Handbook and Resources (GitBook)**
   - URL: [https://robonation.gitbook.io/robosub-resources](https://robonation.gitbook.io/robosub-resources)
   - Sections Consulted:
     - *Section 3: Autonomy Challenge – 3.2 Task Descriptions*
       - URL: [https://robonation.gitbook.io/robosub-resources/section-3-autonomy-challenge/3.2-task-descriptions](https://robonation.gitbook.io/robosub-resources/section-3-autonomy-challenge/3.2-task-descriptions)
     - *Section 5: Rules and Requirements – 5.4 Competition Specifications*
       - URL: [https://robonation.gitbook.io/robosub-resources/section-5-rules-and-requirements/5.4-competition-specifications](https://robonation.gitbook.io/robosub-resources/section-5-rules-and-requirements/5.4-competition-specifications)
     - *Pre-Qualification Course Guidelines*
       - URL: [https://robonation.gitbook.io/robosub-resources/section-3-autonomy-challenge/pre-qualification](https://robonation.gitbook.io/robosub-resources/section-3-autonomy-challenge/pre-qualification)

3. **Gazebo Simulation Documentation**
   - URL: [https://gazebosim.org/docs/harmonic/](https://gazebosim.org/docs/harmonic/)
   - URL: [https://gazebosim.org/docs/harmonic/sdf_worlds/](https://gazebosim.org/docs/harmonic/sdf_worlds/)
   - Key Information: SDFormat 1.9/1.8 specification, Gazebo Sim system plugins (`Physics`, `UserCommands`, `SceneBroadcaster`, `Buoyancy`), rendering, material visual properties.

---

## 2. Categorization of Dimensions and Constraints

To avoid conflating official rules with design assumptions, all parameters are categorized into one of three explicit classes:
1. **[OFFICIAL]**: Explicitly mandated by RoboSub competition rules and specifications.
2. **[DERIVED]**: Estimated from official CAD renderings, competition photos, or task diagrams.
3. **[ASSUMPTION]**: Configurable engineering decision introduced for simulation scale, pool constraints, or numerical stability.

---

## 3. Detailed Task and Element Analysis

### 3.1 Pool Environment
- **[OFFICIAL]** Competition venues historically include the NIWC TRANSDEC facility (San Diego, CA, oval $91\text{ m} \times 61\text{ m} \times 11.6\text{ m}$) or university/regional athletic dive pools (e.g., St. Mary's County Aquatics Center, $25\text{ yd/m}$ dive well with depths between $4\text{ m}$ and $5\text{ m}$).
- **[ASSUMPTION]** Default simulation pool dimensions:
  - Length ($X$): $20.0\text{ m}$
  - Width ($Y$): $10.0\text{ m}$
  - Water Depth ($Z$): $4.0\text{ m}$ (water surface at $z = 4.0\text{ m}$, floor at $z = 0.0\text{ m}$)
  - Wall Thickness: $0.3\text{ m}$, Floor Thickness: $0.3\text{ m}$
  - Wall Height: $4.5\text{ m}$ ($0.5\text{ m}$ freeboard above waterline)
- **Design Rationale:** A $20\text{ m} \times 10\text{ m} \times 4\text{ m}$ rectangular pool provides an optimal balance between realistic AUV maneuvering room and responsive Gazebo rendering performance.

### 3.2 Task 1: Starting Gate (Begin Assessment)
- **[OFFICIAL]** Frame construction: PVC pipe floating just below the surface, moored to the bottom.
- **[OFFICIAL]** Overall frame dimensions: $120\text{ in} \times 60\text{ in}$ ($3.05\text{ m} \times 1.52\text{ m}$).
- **[OFFICIAL]** Leg indicator markings (corrugated plastic markers, 3-inch box sections):
  - Starboard (Right) leg: Upper half RED, lower half BLACK (*"Red, Right, Above"*).
  - Port (Left) leg: Upper half BLACK, lower half RED.
- **[OFFICIAL]** Central vertical divider: 2-inch wide vertical divider splitting the gate into two distinct passage corridors ($1.5\text{ m}$ clear width each), designated for *Survey & Repair* vs. *Search & Rescue* mission pathways.
- **[OFFICIAL]** Pre-qualification gate reference: $2.0\text{ m}$ width, submerged $1.0\text{ m}$ below surface, start position $3.0\text{ m}$ prior.
- **[ASSUMPTION]** Placed at $X = 3.5\text{ m}$, centered at $Y = 0.0\text{ m}$, with gate opening centered at depth $z = 2.5\text{ m}$ ($1.5\text{ m}$ below waterline).

### 3.3 Task 2: Slalom Course (Avoid Debris)
- **[OFFICIAL]** Debris navigation channel composed of vertical PVC pipes moored to the floor at varied heights.
- **[OFFICIAL]** Slalom pipe dimensions: $1\text{-inch}$ nominal PVC pipe ($0.033\text{ m}$ outer diameter), $3\text{ ft}$ ($0.91\text{ m}$) height per segment or vertical floating poles.
- **[OFFICIAL]** Color pattern: Alternating RED and WHITE vertical poles (sets arranged with white on the left/outer bounds and red along center/waypoint boundaries).
- **[ASSUMPTION]** Course configuration: 6 vertical slalom poles staggered along $X = 6.0\text{ m}$ to $X = 11.0\text{ m}$ at $Y = \pm 1.0\text{ m}$ and $Y = 0.0\text{ m}$, with alternating red and white surface coatings to test obstacle avoidance algorithms.

### 3.4 Task 3: Recon Bins
- **[OFFICIAL]** Supported off the pool floor or resting on bottom framework; includes differentiated bins for role tasks (Survey & Repair vs. Search & Rescue).
- **[OFFICIAL]** Dropped markers: Must fit within a $2.0\text{ in} \times 2.0\text{ in} \times 6.0\text{ in}$ ($51 \times 51 \times 152\text{ mm}$) box, max weight $2.0\text{ lbs}$ ($0.91\text{ kg}$).
- **[DERIVED]** Bin dimensions from competition photographs: $0.6\text{ m} \times 0.4\text{ m} \times 0.25\text{ m}$ open top container with high-contrast perimeter borders.
- **[ASSUMPTION]** Placed at $X = 13.5\text{ m}, Y = -1.8\text{ m}$ on the pool floor ($z = 0.15\text{ m}$).

### 3.5 Task 4: Deploy (Torpedo Target Board)
- **[OFFICIAL]** Vertical target board with cutouts for torpedo projectile scoring.
- **[OFFICIAL]** Torpedo projectiles: Max volume $2.0\text{ in} \times 2.0\text{ in} \times 6.0\text{ in}$, weight $\le 2.0\text{ lbs}$.
- **[DERIVED]** Target board cutouts: Two circular/square target apertures (large cutout $\approx 0.30\text{ m}$ diameter, small cutout $\approx 0.15\text{ m}$ diameter) framed with red/black high-contrast borders.
- **[ASSUMPTION]** Vertical board $1.2\text{ m} \times 0.9\text{ m} \times 0.04\text{ m}$, mounted on a weighted bottom stand at $X = 14.0\text{ m}, Y = 2.0\text{ m}$, aperture centerlines at $z = 1.8\text{ m}$ depth.

### 3.6 Task 5: Restore / Resupply & Surfacing Zone (Octagon)
- **[OFFICIAL]** Octagon surface floating/floor perimeter: $9\text{ ft}$ ($2.74\text{ m}$) outer diameter, constructed from $1/2\text{-inch}$ PVC tubing.
- **[OFFICIAL]** Central resupply table: $2\text{ ft} \times 2\text{ ft}$ ($0.61\text{ m} \times 0.61\text{ m}$) frame located within the octagon zone.
- **[OFFICIAL]** Acoustic pinger located on the pool floor in/near the octagon zone operating at $25\text{–}40\text{ kHz}$.
- **[ASSUMPTION]** Octagon zone centered at $X = 17.5\text{ m}, Y = 0.0\text{ m}$ on the pool floor ($z = 0.01\text{ m}$ visual marker) and waterline outline.

### 3.7 Path Navigation Markers
- **[OFFICIAL]** Rectangular orange floor markers: approximately $4\text{ ft}$ ($1.22\text{ m}$) long by $6\text{ in}$ ($0.15\text{ m}$) wide.
- **[OFFICIAL]** Placed after the starting gate and between tasks on the pool bottom angled toward the subsequent mission station.
- **[ASSUMPTION]** 3 path markers distributed along the navigation corridor.

### 3.8 Generic AUV Model (Vehicle Reference)
- **[OFFICIAL]** Competition maximum envelope: $3\text{ ft} \times 3\text{ ft} \times 6\text{ ft}$ ($0.91\text{ m} \times 0.91\text{ m} \times 1.83\text{ m}$), weight limit categories ($<38\text{ kg}$ class 1, up to $56\text{ kg}$).
- **[ASSUMPTION]** Generic AUV placeholder dimensions:
  - Hull: Streamlined torpedo/box body $0.80\text{ m}$ long, $0.40\text{ m}$ wide, $0.30\text{ m}$ high.
  - Forward direction clearly identifiable via front camera dome and forward fin markings.
  - Mass: $25.0\text{ kg}$, neutral buoyancy displacement configuration.
  - Initial pose: $X = 1.0\text{ m}, Y = 0.0\text{ m}, Z = 2.5\text{ m}$, Yaw = $0.0\text{ rad}$ (facing gate).

---

## 4. Visual Appearance and Rendering Specifications
- **Water Palette:** Cyan/deep blue ambient lighting ($R=0.08, G=0.28, B=0.38$) with directional sunlight from overhead.
- **Contrast Rationale:** High-contrast markers (International Orange, Safety Red, Matte Black, Pure White, Signal Yellow) ensure reliable computer vision perception for simulated onboard forward and downward cameras.
- **Collision Rules:**
  - Static structures (pool, gate frame, slalom poles, bins, target boards) include exact simplified geometric bounding boxes or cylinders.
  - Visual path markers and floor zone boundaries are non-colliding (visual only) so they do not impede vehicle dynamics.

---

## 5. Asset Licensing and Attribution
- All core SDFormat models, materials, textures, and scripts are developed under the Apache 2.0 license.
- No proprietary CAD models or closed assets are included. All geometries are procedurally defined or built from open standard primitives for reproducibility.
