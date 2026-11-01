#!/usr/bin/env python3
"""
RoboSub Gazebo Simulation Environment Generator
Reads configuration from config/environment.yaml and generates:
1. Individual modular SDFormat models in models/
2. Master world file worlds/robosub_pool.sdf
3. Visual 2D overhead layout diagram evidence/screenshots/course_layout_overhead.png
"""

import os
import sys
import math
import argparse
import yaml
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_color(color_list):
    return " ".join(f"{c:.4f}" for c in color_list)


def format_pose(pose_list):
    if len(pose_list) == 3:
        return f"{pose_list[0]:.4f} {pose_list[1]:.4f} {pose_list[2]:.4f} 0 0 0"
    elif len(pose_list) == 6:
        return " ".join(f"{p:.4f}" for p in pose_list)
    return "0 0 0 0 0 0"


def generate_pool_model(models_dir, pool_cfg):
    pool_dir = models_dir / "pool"
    pool_dir.mkdir(parents=True, exist_ok=True)

    length = float(pool_cfg["length"])
    width = float(pool_cfg["width"])
    depth = float(pool_cfg["depth"])
    wall_h = float(pool_cfg["wall_height"])
    wall_t = float(pool_cfg["wall_thickness"])
    floor_t = float(pool_cfg["floor_thickness"])
    floor_color = format_color(pool_cfg["floor_material"]["color"])
    wall_color = format_color(pool_cfg["wall_material"]["color"])

    half_l = length / 2.0
    half_w = width / 2.0

    # Config file
    config_xml = f"""<?xml version="1.0"?>
<model>
  <name>pool</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub rectangular competition pool structure</description>
</model>
"""
    with open(pool_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    # SDF file
    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="pool">
    <static>true</static>
    <link name="pool_structure">
      <!-- Floor slab -->
      <visual name="floor_visual">
        <pose>{half_l:.4f} 0 {-floor_t / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {width:.4f} {floor_t:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{floor_color}</ambient>
          <diffuse>{floor_color}</diffuse>
          <specular>0.1 0.1 0.1 1.0</specular>
        </material>
      </visual>
      <collision name="floor_collision">
        <pose>{half_l:.4f} 0 {-floor_t / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {width:.4f} {floor_t:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- Centerline floor navigation tile -->
      <visual name="floor_centerline">
        <pose>{half_l:.4f} 0 0.002 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} 0.15 0.002</size>
          </box>
        </geometry>
        <material>
          <ambient>0.08 0.18 0.22 1.0</ambient>
          <diffuse>0.08 0.18 0.22 1.0</diffuse>
        </material>
      </visual>

      <!-- West Wall (Start Wall, -X) -->
      <visual name="wall_west_visual">
        <pose>{-wall_t / 2.0:.4f} 0 {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{wall_t:.4f} {width + 2 * wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{wall_color}</ambient>
          <diffuse>{wall_color}</diffuse>
        </material>
      </visual>
      <collision name="wall_west_collision">
        <pose>{-wall_t / 2.0:.4f} 0 {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{wall_t:.4f} {width + 2 * wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- East Wall (End Wall, +X) -->
      <visual name="wall_east_visual">
        <pose>{length + wall_t / 2.0:.4f} 0 {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{wall_t:.4f} {width + 2 * wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{wall_color}</ambient>
          <diffuse>{wall_color}</diffuse>
        </material>
      </visual>
      <collision name="wall_east_collision">
        <pose>{length + wall_t / 2.0:.4f} 0 {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{wall_t:.4f} {width + 2 * wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- South Wall (Port Wall, -Y) -->
      <visual name="wall_south_visual">
        <pose>{half_l:.4f} {-half_w - wall_t / 2.0:.4f} {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{wall_color}</ambient>
          <diffuse>{wall_color}</diffuse>
        </material>
      </visual>
      <collision name="wall_south_collision">
        <pose>{half_l:.4f} {-half_w - wall_t / 2.0:.4f} {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- North Wall (Starboard Wall, +Y) -->
      <visual name="wall_north_visual">
        <pose>{half_l:.4f} {half_w + wall_t / 2.0:.4f} {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{wall_color}</ambient>
          <diffuse>{wall_color}</diffuse>
        </material>
      </visual>
      <collision name="wall_north_collision">
        <pose>{half_l:.4f} {half_w + wall_t / 2.0:.4f} {wall_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {wall_t:.4f} {wall_h:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- Water Surface plane marker -->
      <visual name="water_surface_visual">
        <pose>{half_l:.4f} 0 {depth:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{length:.4f} {width:.4f} 0.01</size>
          </box>
        </geometry>
        <material>
          <ambient>0.1 0.45 0.55 0.4</ambient>
          <diffuse>0.15 0.55 0.65 0.4</diffuse>
          <specular>0.6 0.8 0.9 0.6</specular>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
    with open(pool_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_gate_model(models_dir, gate_cfg):
    gate_dir = models_dir / "gate"
    gate_dir.mkdir(parents=True, exist_ok=True)

    w = float(gate_cfg["width"])
    h = float(gate_cfg["height"])
    d = float(gate_cfg["pipe_diameter"])
    r = d / 2.0
    half_w = w / 2.0
    half_h = h / 2.0

    lp_top = format_color(gate_cfg["left_panel"]["top_color"])
    lp_bot = format_color(gate_cfg["left_panel"]["bottom_color"])
    rp_top = format_color(gate_cfg["right_panel"]["top_color"])
    rp_bot = format_color(gate_cfg["right_panel"]["bottom_color"])

    config_xml = """<?xml version="1.0"?>
<model>
  <name>gate</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub competition starting gate with corrugated role marker boxes</description>
</model>
"""
    with open(gate_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="gate">
    <static>true</static>
    <link name="gate_frame">
      <!-- Top Crossbar -->
      <visual name="crossbar_top_visual">
        <pose>0 0 {half_h:.4f} 1.570796 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{w:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.9 0.9 0.9 1.0</ambient>
          <diffuse>0.9 0.9 0.9 1.0</diffuse>
        </material>
      </visual>
      <collision name="crossbar_top_collision">
        <pose>0 0 {half_h:.4f} 1.570796 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{w:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Bottom Crossbar -->
      <visual name="crossbar_bot_visual">
        <pose>0 0 {-half_h:.4f} 1.570796 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{w:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.9 0.9 0.9 1.0</ambient>
          <diffuse>0.9 0.9 0.9 1.0</diffuse>
        </material>
      </visual>
      <collision name="crossbar_bot_collision">
        <pose>0 0 {-half_h:.4f} 1.570796 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{w:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Port Upright (Left, -Y) -->
      <visual name="post_left_visual">
        <pose>0 {-half_w:.4f} 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.9 0.9 0.9 1.0</ambient>
          <diffuse>0.9 0.9 0.9 1.0</diffuse>
        </material>
      </visual>
      <collision name="post_left_collision">
        <pose>0 {-half_w:.4f} 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Starboard Upright (Right, +Y) -->
      <visual name="post_right_visual">
        <pose>0 {half_w:.4f} 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.9 0.9 0.9 1.0</ambient>
          <diffuse>0.9 0.9 0.9 1.0</diffuse>
        </material>
      </visual>
      <collision name="post_right_collision">
        <pose>0 {half_w:.4f} 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Center Divider -->
      <visual name="center_divider_visual">
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.85 0.05 0.05 1.0</ambient>
          <diffuse>0.85 0.05 0.05 1.0</diffuse>
        </material>
      </visual>
      <collision name="center_divider_collision">
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Port Indicator Panel Top (Black) -->
      <visual name="port_panel_top">
        <pose>0 {-half_w:.4f} {half_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>0.12 0.12 {half_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{lp_top}</ambient>
          <diffuse>{lp_top}</diffuse>
        </material>
      </visual>

      <!-- Port Indicator Panel Bottom (Red) -->
      <visual name="port_panel_bot">
        <pose>0 {-half_w:.4f} {-half_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>0.12 0.12 {half_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{lp_bot}</ambient>
          <diffuse>{lp_bot}</diffuse>
        </material>
      </visual>

      <!-- Starboard Indicator Panel Top (Red - "Red Right Above") -->
      <visual name="stbd_panel_top">
        <pose>0 {half_w:.4f} {half_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>0.12 0.12 {half_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{rp_top}</ambient>
          <diffuse>{rp_top}</diffuse>
        </material>
      </visual>

      <!-- Starboard Indicator Panel Bottom (Black) -->
      <visual name="stbd_panel_bot">
        <pose>0 {half_w:.4f} {-half_h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>0.12 0.12 {half_h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{rp_bot}</ambient>
          <diffuse>{rp_bot}</diffuse>
        </material>
      </visual>

      <!-- Mooring tether legs down to pool floor -->
      <visual name="mooring_leg_left">
        <pose>0 {-half_w:.4f} {-half_h - 0.87:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.02</radius>
            <length>1.74</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.4 0.4 0.4 1.0</ambient>
          <diffuse>0.4 0.4 0.4 1.0</diffuse>
        </material>
      </visual>
      <collision name="mooring_leg_left_col">
        <pose>0 {-half_w:.4f} {-half_h - 0.87:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.02</radius>
            <length>1.74</length>
          </cylinder>
        </geometry>
      </collision>

      <visual name="mooring_leg_right">
        <pose>0 {half_w:.4f} {-half_h - 0.87:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.02</radius>
            <length>1.74</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.4 0.4 0.4 1.0</ambient>
          <diffuse>0.4 0.4 0.4 1.0</diffuse>
        </material>
      </visual>
      <collision name="mooring_leg_right_col">
        <pose>0 {half_w:.4f} {-half_h - 0.87:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.02</radius>
            <length>1.74</length>
          </cylinder>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
"""
    with open(gate_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_slalom_pole_model(models_dir, slalom_cfg):
    pole_dir = models_dir / "slalom_pole"
    pole_dir.mkdir(parents=True, exist_ok=True)

    h = float(slalom_cfg["pole_height"])
    d = float(slalom_cfg["pole_diameter"])
    r = d / 2.0
    base_d = float(slalom_cfg.get("base_diameter", 0.4))
    base_r = base_d / 2.0

    config_xml = """<?xml version="1.0"?>
<model>
  <name>slalom_pole</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub vertical slalom course obstacle pole</description>
</model>
"""
    with open(pole_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="slalom_pole">
    <static>true</static>
    <link name="pole_link">
      <!-- Weighted mooring base -->
      <visual name="base_visual">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{base_r:.4f}</radius>
            <length>0.10</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.2 0.2 0.2 1.0</ambient>
          <diffuse>0.2 0.2 0.2 1.0</diffuse>
        </material>
      </visual>
      <collision name="base_collision">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{base_r:.4f}</radius>
            <length>0.10</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Vertical slalom pole body -->
      <visual name="pole_visual">
        <pose>0 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.95 0.95 0.95 1.0</ambient>
          <diffuse>0.95 0.95 0.95 1.0</diffuse>
        </material>
      </visual>
      <collision name="pole_collision">
        <pose>0 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>{r:.4f}</radius>
            <length>{h:.4f}</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- High-visibility pole top cap -->
      <visual name="top_cap_visual">
        <pose>0 0 {h + 0.05:.4f} 0 0 0</pose>
        <geometry>
          <sphere>
            <radius>{r * 1.5:.4f}</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.88 0.08 0.08 1.0</ambient>
          <diffuse>0.88 0.08 0.08 1.0</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
    with open(pole_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_buoy_model(models_dir):
    buoy_dir = models_dir / "buoy"
    buoy_dir.mkdir(parents=True, exist_ok=True)

    config_xml = """<?xml version="1.0"?>
<model>
  <name>buoy</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub spherical identification buoy moored to pool floor</description>
</model>
"""
    with open(buoy_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = """<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="buoy">
    <static>true</static>
    <link name="buoy_link">
      <!-- Floor Anchor -->
      <visual name="anchor_visual">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.25</radius>
            <length>0.10</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.2 0.2 0.2 1.0</ambient>
          <diffuse>0.2 0.2 0.2 1.0</diffuse>
        </material>
      </visual>
      <collision name="anchor_collision">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.25</radius>
            <length>0.10</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Tether cable -->
      <visual name="cable_visual">
        <pose>0 0 1.0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.012</radius>
            <length>2.0</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.3 0.3 0.3 1.0</ambient>
          <diffuse>0.3 0.3 0.3 1.0</diffuse>
        </material>
      </visual>
      <collision name="cable_collision">
        <pose>0 0 1.0 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.012</radius>
            <length>2.0</length>
          </cylinder>
        </geometry>
      </collision>

      <!-- Spherical target buoy body -->
      <visual name="sphere_visual">
        <pose>0 0 2.0 0 0 0</pose>
        <geometry>
          <sphere>
            <radius>0.20</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.9 0.1 0.1 1.0</ambient>
          <diffuse>0.9 0.1 0.1 1.0</diffuse>
        </material>
      </visual>
      <collision name="sphere_collision">
        <pose>0 0 2.0 0 0 0</pose>
        <geometry>
          <sphere>
            <radius>0.20</radius>
          </sphere>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
"""
    with open(buoy_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_target_bin_model(models_dir, bin_cfg):
    bin_dir = models_dir / "target_bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    l = float(bin_cfg.get("length", 1.2))
    w = float(bin_cfg.get("width", 0.8))
    h = float(bin_cfg.get("height", 0.3))
    t = 0.04
    half_l = l / 2.0
    half_w = w / 2.0

    c1 = format_color(bin_cfg.get("bin1_target_color", [0.85, 0.08, 0.08, 1.0]))
    c2 = format_color(bin_cfg.get("bin2_target_color", [0.08, 0.35, 0.85, 1.0]))

    config_xml = """<?xml version="1.0"?>
<model>
  <name>target_bin</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub dual-compartment marker drop target bin</description>
</model>
"""
    with open(bin_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="target_bin">
    <static>true</static>
    <link name="bin_frame">
      <!-- Bottom base plate -->
      <visual name="base_plate_visual">
        <pose>0 0 {t / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{l:.4f} {w:.4f} {t:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>0.15 0.15 0.15 1.0</ambient>
          <diffuse>0.15 0.15 0.15 1.0</diffuse>
        </material>
      </visual>
      <collision name="base_plate_collision">
        <pose>0 0 {t / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{l:.4f} {w:.4f} {t:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- Target symbol 1 (Left compartment - Survey & Repair) -->
      <visual name="target_sym_1">
        <pose>{-half_l / 2.0:.4f} 0 {t + 0.002:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{half_l * 0.7:.4f} {w * 0.7:.4f} 0.002</size>
          </box>
        </geometry>
        <material>
          <ambient>{c1}</ambient>
          <diffuse>{c1}</diffuse>
        </material>
      </visual>

      <!-- Target symbol 2 (Right compartment - Search & Rescue) -->
      <visual name="target_sym_2">
        <pose>{half_l / 2.0:.4f} 0 {t + 0.002:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{half_l * 0.7:.4f} {w * 0.7:.4f} 0.002</size>
          </box>
        </geometry>
        <material>
          <ambient>{c2}</ambient>
          <diffuse>{c2}</diffuse>
        </material>
      </visual>

      <!-- Perimeter Walls -->
      <!-- Wall -X -->
      <visual name="wall_neg_x">
        <pose>{-half_l + t / 2.0:.4f} 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box><size>{t:.4f} {w:.4f} {h:.4f}</size></box>
        </geometry>
        <material><ambient>0.9 0.9 0.9 1.0</ambient><diffuse>0.9 0.9 0.9 1.0</diffuse></material>
      </visual>
      <collision name="col_neg_x">
        <pose>{-half_l + t / 2.0:.4f} 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry><box><size>{t:.4f} {w:.4f} {h:.4f}</size></box></geometry>
      </collision>

      <!-- Wall +X -->
      <visual name="wall_pos_x">
        <pose>{half_l - t / 2.0:.4f} 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box><size>{t:.4f} {w:.4f} {h:.4f}</size></box>
        </geometry>
        <material><ambient>0.9 0.9 0.9 1.0</ambient><diffuse>0.9 0.9 0.9 1.0</diffuse></material>
      </visual>
      <collision name="col_pos_x">
        <pose>{half_l - t / 2.0:.4f} 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry><box><size>{t:.4f} {w:.4f} {h:.4f}</size></box></geometry>
      </collision>

      <!-- Wall -Y -->
      <visual name="wall_neg_y">
        <pose>0 {-half_w + t / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box><size>{l:.4f} {t:.4f} {h:.4f}</size></box>
        </geometry>
        <material><ambient>0.9 0.9 0.9 1.0</ambient><diffuse>0.9 0.9 0.9 1.0</diffuse></material>
      </visual>
      <collision name="col_neg_y">
        <pose>0 {-half_w + t / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><box><size>{l:.4f} {t:.4f} {h:.4f}</size></box></geometry>
      </collision>

      <!-- Wall +Y -->
      <visual name="wall_pos_y">
        <pose>0 {half_w - t / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box><size>{l:.4f} {t:.4f} {h:.4f}</size></box>
        </geometry>
        <material><ambient>0.9 0.9 0.9 1.0</ambient><diffuse>0.9 0.9 0.9 1.0</diffuse></material>
      </visual>
      <collision name="col_pos_y">
        <pose>0 {half_w - t / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><box><size>{l:.4f} {t:.4f} {h:.4f}</size></box></geometry>
      </collision>

      <!-- Center Divider Wall -->
      <visual name="wall_center_div">
        <pose>0 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box><size>{t:.4f} {w:.4f} {h:.4f}</size></box>
        </geometry>
        <material><ambient>0.85 0.05 0.05 1.0</ambient><diffuse>0.85 0.05 0.05 1.0</diffuse></material>
      </visual>
      <collision name="col_center_div">
        <pose>0 0 {h / 2.0:.4f} 0 0 0</pose>
        <geometry><box><size>{t:.4f} {w:.4f} {h:.4f}</size></box></geometry>
      </collision>
    </link>
  </model>
</sdf>
"""
    with open(bin_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_target_board_model(models_dir, board_cfg):
    board_dir = models_dir / "target_board"
    board_dir.mkdir(parents=True, exist_ok=True)

    w = float(board_cfg.get("width", 1.2))
    h = float(board_cfg.get("height", 1.0))
    t = float(board_cfg.get("thickness", 0.04))

    config_xml = """<?xml version="1.0"?>
<model>
  <name>target_board</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub vertical torpedo target board with dual scoring apertures</description>
</model>
"""
    with open(board_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="target_board">
    <static>true</static>
    <link name="board_link">
      <!-- Weighted bottom floor stand -->
      <visual name="stand_base_visual">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry>
          <box><size>0.50 {w * 1.1:.4f} 0.10</size></box>
        </geometry>
        <material><ambient>0.2 0.2 0.2 1.0</ambient><diffuse>0.2 0.2 0.2 1.0</diffuse></material>
      </visual>
      <collision name="stand_base_col">
        <pose>0 0 0.05 0 0 0</pose>
        <geometry><box><size>0.50 {w * 1.1:.4f} 0.10</size></box></geometry>
      </collision>

      <!-- Upright support legs -->
      <visual name="leg_left_visual">
        <pose>0 {-w / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><cylinder><radius>0.03</radius><length>{h + 0.9:.4f}</length></cylinder></geometry>
        <material><ambient>0.8 0.8 0.8 1.0</ambient><diffuse>0.8 0.8 0.8 1.0</diffuse></material>
      </visual>
      <collision name="leg_left_col">
        <pose>0 {-w / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><cylinder><radius>0.03</radius><length>{h + 0.9:.4f}</length></cylinder></geometry>
      </collision>

      <visual name="leg_right_visual">
        <pose>0 {w / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><cylinder><radius>0.03</radius><length>{h + 0.9:.4f}</length></cylinder></geometry>
        <material><ambient>0.8 0.8 0.8 1.0</ambient><diffuse>0.8 0.8 0.8 1.0</diffuse></material>
      </visual>
      <collision name="leg_right_col">
        <pose>0 {w / 2.0:.4f} {h / 2.0:.4f} 0 0 0</pose>
        <geometry><cylinder><radius>0.03</radius><length>{h + 0.9:.4f}</length></cylinder></geometry>
      </collision>

      <!-- Main Faceboard panel -->
      <visual name="board_face_visual">
        <pose>0 0 {h:.4f} 0 0 0</pose>
        <geometry><box><size>{t:.4f} {w:.4f} {h:.4f}</size></box></geometry>
        <material><ambient>0.92 0.92 0.92 1.0</ambient><diffuse>0.92 0.92 0.92 1.0</diffuse></material>
      </visual>
      <collision name="board_face_col">
        <pose>0 0 {h:.4f} 0 0 0</pose>
        <geometry><box><size>{t:.4f} {w:.4f} {h:.4f}</size></box></geometry>
      </collision>

      <!-- Target 1 (Large 30cm cutout simulation disc) -->
      <visual name="large_target_ring">
        <pose>{t / 2.0 + 0.002:.4f} {-w / 4.0:.4f} {h:.4f} 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.15</radius><length>0.005</length></cylinder></geometry>
        <material><ambient>0.85 0.05 0.05 1.0</ambient><diffuse>0.85 0.05 0.05 1.0</diffuse></material>
      </visual>
      <visual name="large_target_center">
        <pose>{t / 2.0 + 0.004:.4f} {-w / 4.0:.4f} {h:.4f} 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.06</radius><length>0.005</length></cylinder></geometry>
        <material><ambient>0.05 0.05 0.05 1.0</ambient><diffuse>0.05 0.05 0.05 1.0</diffuse></material>
      </visual>

      <!-- Target 2 (Small 15cm cutout simulation disc) -->
      <visual name="small_target_ring">
        <pose>{t / 2.0 + 0.002:.4f} {w / 4.0:.4f} {h:.4f} 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.09</radius><length>0.005</length></cylinder></geometry>
        <material><ambient>0.1 0.4 0.9 1.0</ambient><diffuse>0.1 0.4 0.9 1.0</diffuse></material>
      </visual>
      <visual name="small_target_center">
        <pose>{t / 2.0 + 0.004:.4f} {w / 4.0:.4f} {h:.4f} 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.035</radius><length>0.005</length></cylinder></geometry>
        <material><ambient>0.05 0.05 0.05 1.0</ambient><diffuse>0.05 0.05 0.05 1.0</diffuse></material>
      </visual>
    </link>
  </model>
</sdf>
"""
    with open(board_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_octagon_zone_model(models_dir, oct_cfg):
    oct_dir = models_dir / "octagon_zone"
    oct_dir.mkdir(parents=True, exist_ok=True)

    diam = float(oct_cfg.get("diameter", 2.74))
    r = diam / 2.0
    seg_w = float(oct_cfg.get("border_thickness", 0.08))
    oct_color = format_color(oct_cfg.get("color", [1.0, 0.45, 0.0, 1.0]))

    side_len = 2.0 * r * math.sin(math.pi / 8.0)

    config_xml = """<?xml version="1.0"?>
<model>
  <name>octagon_zone</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub 9ft octagonal surfacing/resupply zone with central table and pinger</description>
</model>
"""
    with open(oct_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    segments_xml = ""
    for i in range(8):
        angle = i * (2.0 * math.pi / 8.0)
        seg_dist = r * math.cos(math.pi / 8.0)
        px = seg_dist * math.cos(angle)
        py = seg_dist * math.sin(angle)
        yaw = angle + math.pi / 2.0
        segments_xml += f"""
      <!-- Octagon perimeter segment {i+1} -->
      <visual name="oct_seg_{i+1}">
        <pose>{px:.4f} {py:.4f} 0.005 0 0 {yaw:.4f}</pose>
        <geometry>
          <box>
            <size>{side_len:.4f} {seg_w:.4f} 0.005</size>
          </box>
        </geometry>
        <material>
          <ambient>{oct_color}</ambient>
          <diffuse>{oct_color}</diffuse>
        </material>
      </visual>"""

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="octagon_zone">
    <static>true</static>
    <link name="octagon_link">
      {segments_xml}

      <!-- Center Floor Crosshair -->
      <visual name="crosshair_x">
        <pose>0 0 0.006 0 0 0</pose>
        <geometry><box><size>0.80 0.04 0.004</size></box></geometry>
        <material><ambient>1.0 1.0 1.0 1.0</ambient><diffuse>1.0 1.0 1.0 1.0</diffuse></material>
      </visual>
      <visual name="crosshair_y">
        <pose>0 0 0.006 0 0 1.570796</pose>
        <geometry><box><size>0.80 0.04 0.004</size></box></geometry>
        <material><ambient>1.0 1.0 1.0 1.0</ambient><diffuse>1.0 1.0 1.0 1.0</diffuse></material>
      </visual>

      <!-- Central Resupply Table (2ft x 2ft) -->
      <visual name="resupply_table_top">
        <pose>0 0 0.30 0 0 0</pose>
        <geometry><box><size>0.61 0.61 0.04</size></box></geometry>
        <material><ambient>0.85 0.85 0.85 1.0</ambient><diffuse>0.85 0.85 0.85 1.0</diffuse></material>
      </visual>
      <collision name="resupply_table_top_col">
        <pose>0 0 0.30 0 0 0</pose>
        <geometry><box><size>0.61 0.61 0.04</size></box></geometry>
      </collision>

      <!-- Table Legs -->
      <visual name="table_leg_1">
        <pose>-0.25 -0.25 0.15 0 0 0</pose>
        <geometry><cylinder><radius>0.02</radius><length>0.30</length></cylinder></geometry>
        <material><ambient>0.3 0.3 0.3 1.0</ambient><diffuse>0.3 0.3 0.3 1.0</diffuse></material>
      </visual>
      <visual name="table_leg_2">
        <pose>0.25 -0.25 0.15 0 0 0</pose>
        <geometry><cylinder><radius>0.02</radius><length>0.30</length></cylinder></geometry>
        <material><ambient>0.3 0.3 0.3 1.0</ambient><diffuse>0.3 0.3 0.3 1.0</diffuse></material>
      </visual>
      <visual name="table_leg_3">
        <pose>-0.25 0.25 0.15 0 0 0</pose>
        <geometry><cylinder><radius>0.02</radius><length>0.30</length></cylinder></geometry>
        <material><ambient>0.3 0.3 0.3 1.0</ambient><diffuse>0.3 0.3 0.3 1.0</diffuse></material>
      </visual>
      <visual name="table_leg_4">
        <pose>0.25 0.25 0.15 0 0 0</pose>
        <geometry><cylinder><radius>0.02</radius><length>0.30</length></cylinder></geometry>
        <material><ambient>0.3 0.3 0.3 1.0</ambient><diffuse>0.3 0.3 0.3 1.0</diffuse></material>
      </visual>

      <!-- Acoustic Pinger Transducer Placeholder -->
      <visual name="pinger_housing">
        <pose>0 0 0.34 0 0 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.08</length></cylinder></geometry>
        <material><ambient>0.1 0.1 0.1 1.0</ambient><diffuse>0.1 0.1 0.1 1.0</diffuse></material>
      </visual>
      <visual name="pinger_emitter_cap">
        <pose>0 0 0.39 0 0 0</pose>
        <geometry><sphere><radius>0.04</radius></sphere></geometry>
        <material><ambient>0.95 0.85 0.05 1.0</ambient><diffuse>0.95 0.85 0.05 1.0</diffuse></material>
      </visual>
      <collision name="pinger_col">
        <pose>0 0 0.35 0 0 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.10</length></cylinder></geometry>
      </collision>
    </link>
  </model>
</sdf>
"""
    with open(oct_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_path_marker_model(models_dir, path_cfg):
    marker_dir = models_dir / "path_marker"
    marker_dir.mkdir(parents=True, exist_ok=True)

    dims = path_cfg.get("dimensions", [1.22, 0.15, 0.01])
    color = format_color(path_cfg.get("color", [1.0, 0.45, 0.0, 1.0]))

    config_xml = """<?xml version="1.0"?>
<model>
  <name>path_marker</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub high-visibility orange navigation path marker</description>
</model>
"""
    with open(marker_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="path_marker">
    <static>true</static>
    <link name="marker_link">
      <visual name="marker_visual">
        <pose>0 0 {dims[2] / 2.0:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{dims[0]:.4f} {dims[1]:.4f} {dims[2]:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{color}</ambient>
          <diffuse>{color}</diffuse>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""
    with open(marker_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_auv_model(models_dir, auv_cfg):
    auv_dir = models_dir / "auv_placeholder"
    auv_dir.mkdir(parents=True, exist_ok=True)

    l = float(auv_cfg.get("length", 0.80))
    w = float(auv_cfg.get("width", 0.40))
    h = float(auv_cfg.get("height", 0.30))
    mass = float(auv_cfg.get("mass", 25.0))
    hull_color = format_color(auv_cfg.get("hull_color", [0.95, 0.80, 0.05, 1.0]))

    ixx = (1.0 / 12.0) * mass * (w * w + h * h)
    iyy = (1.0 / 12.0) * mass * (l * l + h * h)
    izz = (1.0 / 12.0) * mass * (l * l + w * w)

    config_xml = """<?xml version="1.0"?>
<model>
  <name>auv_placeholder</name>
  <version>1.0</version>
  <sdf version="1.9">model.sdf</sdf>
  <author>
    <name>RoboSub Simulation Team</name>
  </author>
  <description>RoboSub generic autonomous underwater vehicle reference model</description>
</model>
"""
    with open(auv_dir / "model.config", "w", encoding="utf-8") as f:
        f.write(config_xml)

    sdf_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <model name="auv_placeholder">
    <static>false</static>
    <link name="base_link">
      <inertial>
        <mass>{mass:.4f}</mass>
        <inertia>
          <ixx>{ixx:.4f}</ixx><ixy>0</ixy><ixz>0</ixz>
          <iyy>{iyy:.4f}</iyy><iyz>0</iyz>
          <izz>{izz:.4f}</izz>
        </inertia>
      </inertial>

      <!-- Main Hull body -->
      <visual name="hull_visual">
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <box>
            <size>{l:.4f} {w:.4f} {h:.4f}</size>
          </box>
        </geometry>
        <material>
          <ambient>{hull_color}</ambient>
          <diffuse>{hull_color}</diffuse>
          <specular>0.3 0.3 0.3 1.0</specular>
        </material>
      </visual>
      <collision name="hull_collision">
        <pose>0 0 0 0 0 0</pose>
        <geometry>
          <box>
            <size>{l:.4f} {w:.4f} {h:.4f}</size>
          </box>
        </geometry>
      </collision>

      <!-- Forward Optical Sensor Dome (Heading indicator) -->
      <visual name="bow_dome_visual">
        <pose>{l / 2.0:.4f} 0 0 0 1.570796 0</pose>
        <geometry>
          <sphere>
            <radius>{h / 2.5:.4f}</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.1 0.1 0.1 0.8</ambient>
          <diffuse>0.1 0.1 0.1 0.8</diffuse>
          <specular>0.8 0.8 0.8 1.0</specular>
        </material>
      </visual>

      <!-- Heading Directional Arrow on Top Deck -->
      <visual name="heading_arrow">
        <pose>{l / 4.0:.4f} 0 {h / 2.0 + 0.005:.4f} 0 0 0</pose>
        <geometry>
          <box>
            <size>{l / 3.0:.4f} 0.05 0.005</size>
          </box>
        </geometry>
        <material>
          <ambient>0.85 0.05 0.05 1.0</ambient>
          <diffuse>0.85 0.05 0.05 1.0</diffuse>
        </material>
      </visual>

      <!-- Downward Camera Well -->
      <visual name="down_cam_visual">
        <pose>0 0 {-h / 2.0 - 0.02:.4f} 0 0 0</pose>
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.04</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.1 0.1 0.1 1.0</ambient>
          <diffuse>0.1 0.1 0.1 1.0</diffuse>
        </material>
      </visual>

      <!-- Port Thruster Ducts -->
      <visual name="thruster_port_visual">
        <pose>0 {-w / 2.0 - 0.06:.4f} 0 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.16</length></cylinder></geometry>
        <material><ambient>0.15 0.15 0.15 1.0</ambient><diffuse>0.15 0.15 0.15 1.0</diffuse></material>
      </visual>
      <collision name="thruster_port_col">
        <pose>0 {-w / 2.0 - 0.06:.4f} 0 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.16</length></cylinder></geometry>
      </collision>

      <!-- Starboard Thruster Ducts -->
      <visual name="thruster_stbd_visual">
        <pose>0 {w / 2.0 + 0.06:.4f} 0 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.16</length></cylinder></geometry>
        <material><ambient>0.15 0.15 0.15 1.0</ambient><diffuse>0.15 0.15 0.15 1.0</diffuse></material>
      </visual>
      <collision name="thruster_stbd_col">
        <pose>0 {w / 2.0 + 0.06:.4f} 0 0 1.570796 0</pose>
        <geometry><cylinder><radius>0.05</radius><length>0.16</length></cylinder></geometry>
      </collision>
    </link>
  </model>
</sdf>
"""
    with open(auv_dir / "model.sdf", "w", encoding="utf-8") as f:
        f.write(sdf_xml)


def generate_world_sdf(output_world_path, config):
    lighting = config["lighting"]
    ambient_str = format_color(lighting["ambient"])
    bg_str = format_color(lighting["background"])
    sun_dir = " ".join(str(x) for x in lighting["sun"]["direction"])
    sun_diff = format_color(lighting["sun"]["diffuse"])
    sun_spec = format_color(lighting["sun"]["specular"])

    gate_pose = format_pose(config["gate"]["position"])
    bins_pose = format_pose(config["bins"]["position"])
    target_board_pose = f"{config['target_board']['position'][0]:.4f} {config['target_board']['position'][1]:.4f} {config['target_board']['position'][2]:.4f} {config['target_board']['rotation'][0]:.4f} {config['target_board']['rotation'][1]:.4f} {config['target_board']['rotation'][2]:.4f}"
    octagon_pose = format_pose(config["octagon_zone"]["position"])
    auv_pose = format_pose(config["auv_placeholder"]["start_pose"])

    # Slalom poles
    slalom_includes = ""
    for pole in config["slalom"]["poles"]:
        pole_id = pole["id"]
        pos = pole["position"]
        col = format_color(pole["color"])
        slalom_includes += f"""
    <!-- {pole_id} -->
    <include>
      <name>{pole_id}</name>
      <uri>model://slalom_pole</uri>
      <pose>{pos[0]:.4f} {pos[1]:.4f} 0 0 0 0</pose>
    </include>"""

    # Buoys
    buoy_includes = ""
    for b in config["buoys"]:
        b_id = b["id"]
        pos = b["position"]
        buoy_includes += f"""
    <!-- {b_id} -->
    <include>
      <name>{b_id}</name>
      <uri>model://buoy</uri>
      <pose>{pos[0]:.4f} {pos[1]:.4f} 0 0 0 0</pose>
    </include>"""

    # Path markers
    path_includes = ""
    for pm in config["path_markers"]["markers"]:
        pm_id = pm["id"]
        pos = pm["position"]
        yaw = pm.get("yaw", 0.0)
        path_includes += f"""
    <!-- {pm_id} -->
    <include>
      <name>{pm_id}</name>
      <uri>model://path_marker</uri>
      <pose>{pos[0]:.4f} {pos[1]:.4f} {pos[2]:.4f} 0 0 {yaw:.4f}</pose>
    </include>"""

    world_xml = f"""<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="robosub_pool_world">
    <!-- Physics parameters -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Core Gazebo Sim System Plugins -->
    <plugin
      filename="gz-sim-physics-system"
      name="gz::sim::systems::Physics">
    </plugin>
    <plugin
      filename="gz-sim-user-commands-system"
      name="gz::sim::systems::UserCommands">
    </plugin>
    <plugin
      filename="gz-sim-scene-broadcaster-system"
      name="gz::sim::systems::SceneBroadcaster">
    </plugin>
    <plugin
      filename="gz-sim-buoyancy-system"
      name="gz::sim::systems::Buoyancy">
      <uniform_fluid_density>1000.0</uniform_fluid_density>
    </plugin>

    <!-- Underwater Scene & Lighting settings -->
    <scene>
      <ambient>{ambient_str}</ambient>
      <background>{bg_str}</background>
      <shadows>true</shadows>
      <grid>false</grid>
    </scene>

    <!-- Surface Penetrating Sunlight -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>10.0 0.0 10.0 0 0 0</pose>
      <diffuse>{sun_diff}</diffuse>
      <specular>{sun_spec}</specular>
      <direction>{sun_dir}</direction>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
    </light>

    <!-- Underwater Pool Model -->
    <include>
      <name>pool</name>
      <uri>model://pool</uri>
      <pose>0 0 0 0 0 0</pose>
    </include>

    <!-- Starting Gate -->
    <include>
      <name>starting_gate</name>
      <uri>model://gate</uri>
      <pose>{gate_pose}</pose>
    </include>

    <!-- Slalom Obstacle Poles -->
    {slalom_includes}

    <!-- Buoys -->
    {buoy_includes}

    <!-- Path Navigation Markers -->
    {path_includes}

    <!-- Recon Target Bins -->
    <include>
      <name>target_bins</name>
      <uri>model://target_bin</uri>
      <pose>{bins_pose}</pose>
    </include>

    <!-- Torpedo Target Board -->
    <include>
      <name>target_board</name>
      <uri>model://target_board</uri>
      <pose>{target_board_pose}</pose>
    </include>

    <!-- Octagonal Mission / Resupply Zone -->
    <include>
      <name>octagon_zone</name>
      <uri>model://octagon_zone</uri>
      <pose>{octagon_pose}</pose>
    </include>

    <!-- Generic AUV Model Placeholder -->
    <include>
      <name>auv_reference</name>
      <uri>model://auv_placeholder</uri>
      <pose>{auv_pose}</pose>
    </include>
  </world>
</sdf>
"""
    output_world_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_world_path, "w", encoding="utf-8") as f:
        f.write(world_xml)


def generate_overhead_diagram(output_img_path, config):
    if not HAVE_MATPLOTLIB:
        print("matplotlib not available; skipping diagram generation.")
        return

    output_img_path.parent.mkdir(parents=True, exist_ok=True)

    pool = config["pool"]
    length = float(pool["length"])
    width = float(pool["width"])

    fig, ax = plt.subplots(figsize=(14, 7), dpi=150)
    ax.set_facecolor("#113344")

    # Pool boundary
    pool_rect = patches.Rectangle((0, -width / 2.0), length, width, linewidth=3, edgecolor="#22ccdd", facecolor="#0e2a38")
    ax.add_patch(pool_rect)

    # Centerline
    ax.plot([0, length], [0, 0], color="#1c5068", linestyle="--", linewidth=1.5, label="Course Centerline")

    # AUV start
    auv_pose = config["auv_placeholder"]["start_pose"]
    ax.plot(auv_pose[0], auv_pose[1], "y^", markersize=14, label="AUV Start (1.0m, 0.0m)")
    ax.text(auv_pose[0], auv_pose[1] + 0.4, "AUV Start", color="#ffdd00", fontsize=9, fontweight="bold", ha="center")

    # Starting Gate
    gate_pos = config["gate"]["position"]
    gw = float(config["gate"]["width"])
    ax.plot([gate_pos[0], gate_pos[0]], [gate_pos[1] - gw / 2.0, gate_pos[1] + gw / 2.0], color="#ff3333", linewidth=4, label="Starting Gate (3.5m)")
    ax.text(gate_pos[0], gate_pos[1] + gw / 2.0 + 0.3, "Gate (3.05m x 1.52m)", color="#ff6666", fontsize=9, ha="center")

    # Slalom Poles
    for p in config["slalom"]["poles"]:
        pos = p["position"]
        col = "#ffffff" if p["color"][0] > 0.9 and p["color"][1] > 0.9 else "#ee2222"
        ax.plot(pos[0], pos[1], marker="o", color=col, markersize=8, markeredgecolor="black")
        ax.text(pos[0], pos[1] + 0.3, p["id"].replace("slalom_", ""), color=col, fontsize=7, ha="center")

    # Buoys
    for b in config["buoys"]:
        pos = b["position"]
        b_col = tuple(b["color"][:3])
        ax.plot(pos[0], pos[1], marker="o", color=b_col, markersize=10, markeredgecolor="black")
        ax.text(pos[0], pos[1] - 0.4, b["id"].replace("buoy_", "buoy "), color=b_col, fontsize=8, ha="center")

    # Bins
    bin_pos = config["bins"]["position"]
    bl = float(config["bins"]["length"])
    bw = float(config["bins"]["width"])
    bin_rect = patches.Rectangle((bin_pos[0] - bl / 2.0, bin_pos[1] - bw / 2.0), bl, bw, linewidth=1.5, edgecolor="#ffffff", facecolor="#222222")
    ax.add_patch(bin_rect)
    ax.text(bin_pos[0], bin_pos[1], "Recon Bins", color="#ffffff", fontsize=8, ha="center", va="center")

    # Target Board
    tb_pos = config["target_board"]["position"]
    tw = float(config["target_board"]["width"])
    ax.plot([tb_pos[0], tb_pos[0]], [tb_pos[1] - tw / 2.0, tb_pos[1] + tw / 2.0], color="#00ffcc", linewidth=4, label="Target Board")
    ax.text(tb_pos[0], tb_pos[1] + tw / 2.0 + 0.3, "Torpedo Board", color="#00ffcc", fontsize=8, ha="center")

    # Path markers
    for pm in config["path_markers"]["markers"]:
        pos = pm["position"]
        yaw = pm.get("yaw", 0.0)
        ax.arrow(pos[0], pos[1], 0.6 * math.cos(yaw), 0.6 * math.sin(yaw), head_width=0.2, head_length=0.2, fc="#ff8800", ec="#ff8800")

    # Octagon Zone
    oct_pos = config["octagon_zone"]["position"]
    oct_diam = float(config["octagon_zone"]["diameter"])
    oct_patch = patches.RegularPolygon((oct_pos[0], oct_pos[1]), numVertices=8, radius=oct_diam / 2.0, orientation=0, edgecolor="#ff7700", facecolor="none", linewidth=2.5)
    ax.add_patch(oct_patch)
    ax.plot(oct_pos[0], oct_pos[1], "r+", markersize=12)
    ax.text(oct_pos[0], oct_pos[1] + oct_diam / 2.0 + 0.3, "Octagon Zone (9ft)", color="#ff7700", fontsize=9, fontweight="bold", ha="center")

    # Styling and limits
    ax.set_xlim(-1.5, length + 1.5)
    ax.set_ylim(-width / 2.0 - 1.0, width / 2.0 + 1.0)
    ax.set_xlabel("X Coordinate (Downrange Course Direction) [meters]", color="#cceeff", fontsize=11)
    ax.set_ylabel("Y Coordinate (Lateral Axis) [meters]", color="#cceeff", fontsize=11)
    ax.set_title("RoboSub Underwater Competition Simulation Environment Layout (Top-Down)", color="#ffffff", fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors="#cceeff")
    ax.grid(True, color="#1a4455", linestyle=":", alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_img_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated layout diagram: {output_img_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate RoboSub Gazebo environment from config")
    parser.add_argument("--config", default="config/environment.yaml", help="Path to environment YAML")
    parser.add_argument("--output", default="worlds/robosub_pool.sdf", help="Output world SDF file")
    parser.add_argument("--models-dir", default="models", help="Output models directory")
    parser.add_argument("--diagram", default="evidence/screenshots/course_layout_overhead.png", help="Output diagram path")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / args.config
    output_world = project_root / args.output
    models_dir = project_root / args.models_dir
    diagram_path = project_root / args.diagram

    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    print(f"Loading configuration from {config_path}...")
    config = load_config(config_path)

    print(f"Generating modular models in {models_dir}...")
    generate_pool_model(models_dir, config["pool"])
    generate_gate_model(models_dir, config["gate"])
    generate_slalom_pole_model(models_dir, config["slalom"])
    generate_buoy_model(models_dir)
    generate_target_bin_model(models_dir, config["bins"])
    generate_target_board_model(models_dir, config["target_board"])
    generate_octagon_zone_model(models_dir, config["octagon_zone"])
    generate_path_marker_model(models_dir, config["path_markers"])
    generate_auv_model(models_dir, config["auv_placeholder"])

    print(f"Generating world SDF at {output_world}...")
    generate_world_sdf(output_world, config)

    print(f"Generating layout diagram at {diagram_path}...")
    generate_overhead_diagram(diagram_path, config)

    print("Generation complete successfully.")


if __name__ == "__main__":
    main()
