# RoboSub Competition Course Layout

## 1. Overhead Course Schematic

```
====================================================================================================
                              ROBOSUB COMPETITION POOL (20m x 10m x 4m)
====================================================================================================
Y (m)
 +5.0 ┌────────────────────────────────────────────────────────────────────────────────────────┐
      │                                                                                        │
 +4.0 │                                                                                        │
      │                                                                                        │
 +3.0 │                                                                                        │
      │                                                                                        │
 +2.0 │                                                 [TARGET BOARD]                         │
      │                                                 (14.2, +2.0)                           │
 +1.0 │                       (P3) White       (P6) White                                      │
      │                      (8.5, +1.0)      (11.5, +1.0)                                     │
      │                                                                      [OCTAGON ZONE]    │
  0.0 │ [START]     [GATE]         (P2) Red         (P5) Red                 (17.5, 0.0)       │
      │  (1.0)     (3.5, 0.0)     (7.5, 0.0)      (10.5, 0.0)                  Pinger &        │
      │  AUV           ║                                                       Resupply        │
 -1.0 │                ║      (P1) White       (P4) White                       Table          │
      │                ║     (6.5, -1.0)      (9.5, -1.0)                                      │
 -2.0 │                ║                                      [BINS]                           │
      │                ║                        [BUOY ARRAY] (14.0, -2.0)                      │
 -3.0 │                                         (12.8, -1.8)                                   │
      │                                                                                        │
 -4.0 │                                                                                        │
      │                                                                                        │
 -5.0 └────────────────────────────────────────────────────────────────────────────────────────┘
       0.0    1.0   2.0   3.0   4.0   5.0   6.0   7.0   8.0   9.0  10.0  11.0  12.0  13.0  14.0  15.0  16.0  17.0  18.0  19.0  20.0
                                                     X (m) ->
```

---

## 2. Element Coordinates and Specifications Table

| Station / Element | Type / Description | Coordinates $(X, Y, Z)$ [m] | Orientation / Size | Clearance / Passage |
| :--- | :--- | :--- | :--- | :--- |
| **Start Point** | AUV Initial Placement | $(1.0, 0.0, 2.5)$ | Heading: $+X$ ($0^\circ$) | Free start box $2.5\text{ m}$ clearance to gate |
| **Task 1: Starting Gate** | 120"x60" PVC Gate with Port/Stbd Box Markers | $(3.5, 0.0, 2.5)$ | Normal: $+X$, Submerged $1.5\text{ m}$ | Dual channels, $1.5\text{ m}$ width each |
| **Path Marker 1** | High-vis Orange Navigation Strip | $(4.8, 0.0, 0.01)$ | Heading: $+X$ ($0.0\text{ rad}$) | Floor level ($1.22\text{ m} \times 0.15\text{ m}$) |
| **Task 2: Slalom Pole 1** | Vertical PVC Pole (White) | $(6.5, -1.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Lateral spacing $1.0\text{ m}$ |
| **Task 2: Slalom Pole 2** | Vertical PVC Pole (Red) | $(7.5, 0.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Longitudinal spacing $1.0\text{ m}$ |
| **Task 2: Slalom Pole 3** | Vertical PVC Pole (White) | $(8.5, 1.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Lateral spacing $1.0\text{ m}$ |
| **Task 2: Slalom Pole 4** | Vertical PVC Pole (White) | $(9.5, -1.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Longitudinal spacing $1.0\text{ m}$ |
| **Task 2: Slalom Pole 5** | Vertical PVC Pole (Red) | $(10.5, 0.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Alternating red/white slalom track |
| **Task 2: Slalom Pole 6** | Vertical PVC Pole (White) | $(11.5, 1.0, 1.1)$ | Height $2.2\text{ m}$, Diam $0.06\text{ m}$ | Exit to mission stations |
| **Path Marker 2** | High-vis Orange Navigation Strip | $(12.2, -0.6, 0.01)$ | Yaw: $-0.45\text{ rad}$ | Directs vehicle toward bins |
| **Task 3: Buoy Array (Red)** | Red Spherical Identification Buoy | $(12.8, -1.8, 2.0)$ | Diameter $0.40\text{ m}$ | Mid-depth buoy target |
| **Task 3: Buoy Array (Green)**| Green Spherical Identification Buoy | $(12.8, -0.9, 2.0)$ | Diameter $0.40\text{ m}$ | Mid-depth buoy target |
| **Task 3: Buoy Array (Yellow)**| Yellow Spherical Identification Buoy| $(12.8, 0.0, 2.0)$ | Diameter $0.40\text{ m}$ | Mid-depth buoy target |
| **Task 4: Recon Bins** | Dual-compartment Floor Target Bins | $(14.0, -2.0, 0.15)$ | $1.2\text{ m} \times 0.8\text{ m} \times 0.3\text{ m}$ | Marker drop target area |
| **Task 5: Torpedo Board** | Vertical Target Board with 2 Apertures | $(14.2, 2.0, 1.5)$ | Apertures: $0.3\text{ m}$ & $0.15\text{ m}$ | Frontal standoff range $> 1.0\text{ m}$ |
| **Path Marker 3** | High-vis Orange Navigation Strip | $(15.8, 0.0, 0.01)$ | Yaw: $+0.35\text{ rad}$ | Directs vehicle toward Octagon |
| **Task 6: Octagon Zone** | $9\text{ ft}$ Diameter Floor Surfacing Perimeter| $(17.5, 0.0, 0.015)$ | Outer Diameter $2.74\text{ m}$ | Surfacing and homing area |
| **Task 6: Resupply Table** | Central Platform & Items | $(17.5, 0.0, 0.30)$ | $0.61\text{ m} \times 0.61\text{ m}$ | Center of Octagon |
| **Task 6: Acoustic Pinger** | Pinger Transducer Placeholder | $(17.5, 0.0, 0.05)$ | Floor acoustic beacon | Center of Octagon |

---

## 3. Autonomous Navigation Corridors

The course layout defines a sequence of distinct autonomy challenge segments:
1. **Start & Gate Ingress ($X = 1.0\text{ m} \to 4.0\text{ m}$):** Vehicle begins at submerged depth $z = 2.5\text{ m}$, trims buoyancy, detects gate uprights via front stereo vision, and selects either the port (*Search & Rescue*) or starboard (*Survey & Repair*) corridor based on mission objectives.
2. **Debris Slalom ($X = 6.0\text{ m} \to 12.0\text{ m}$):** Vehicle navigates through the alternating red and white pole obstacles, utilizing active obstacle avoidance (sonar / depth camera). Minimum clearance between poles is $> 1.4\text{ m}$ diagonally.
3. **Task Splitting Junction ($X = 12.0\text{ m} \to 15.0\text{ m}$):**
   - **Port Trajectory ($-Y$):** Directs to Recon Bins for downward camera marker release and buoy color classification.
   - **Starboard Trajectory ($+Y$):** Directs to Torpedo Board for visual alignment and projectile firing.
4. **Terminal Homing & Surfacing ($X = 15.0\text{ m} \to 19.0\text{ m}$):** Both trajectories converge on the $2.74\text{ m}$ diameter Octagon Zone guided by path markers and the acoustic pinger beacon.
