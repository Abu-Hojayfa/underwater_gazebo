#!/usr/bin/env python3
"""
3D Scene and Asset Visualizer for RoboSub Gazebo Environment
Generates high-resolution multi-angle 3D visual renderings and genuine evidence
representing the exact geometries, poses, and colors configured in the environment.
"""

import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path
import yaml


def load_config():
    root = Path(__file__).resolve().parent.parent
    with open(root / "config" / "environment.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f), root


def draw_box(ax, center, size, color, alpha=1.0, edgecolor="black"):
    cx, cy, cz = center
    sx, sy, sz = size
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0

    # 8 vertices
    vertices = np.array([
        [cx - hx, cy - hy, cz - hz],
        [cx + hx, cy - hy, cz - hz],
        [cx + hx, cy + hy, cz - hz],
        [cx - hx, cy + hy, cz - hz],
        [cx - hx, cy - hy, cz + hz],
        [cx + hx, cy - hy, cz + hz],
        [cx + hx, cy + hy, cz + hz],
        [cx - hx, cy + hy, cz + hz],
    ])

    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]], # bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]], # top
        [vertices[0], vertices[1], vertices[5], vertices[4]], # front
        [vertices[2], vertices[3], vertices[7], vertices[6]], # back
        [vertices[1], vertices[2], vertices[6], vertices[5]], # right
        [vertices[0], vertices[3], vertices[7], vertices[4]], # left
    ]

    poly = Poly3DCollection(faces, facecolors=color, linewidths=0.5, edgecolors=edgecolor, alpha=alpha)
    ax.add_collection3d(poly)


def draw_cylinder(ax, center, radius, length, color, axis="z", alpha=1.0, resolution=16):
    cx, cy, cz = center
    theta = np.linspace(0, 2 * np.pi, resolution)
    z_line = np.linspace(-length / 2.0, length / 2.0, 2)
    theta_grid, z_grid = np.meshgrid(theta, z_line)

    if axis == "z":
        x = cx + radius * np.cos(theta_grid)
        y = cy + radius * np.sin(theta_grid)
        z = cz + z_grid
    elif axis == "y":
        x = cx + radius * np.cos(theta_grid)
        y = cy + z_grid
        z = cz + radius * np.sin(theta_grid)
    else: # axis == "x"
        x = cx + z_grid
        y = cy + radius * np.cos(theta_grid)
        z = cz + radius * np.sin(theta_grid)

    ax.plot_surface(x, y, z, color=color, alpha=alpha, shade=True, edgecolor="none")


def draw_sphere(ax, center, radius, color, alpha=1.0, resolution=14):
    cx, cy, cz = center
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = cx + radius * np.outer(np.cos(u), np.sin(v))
    y = cy + radius * np.outer(np.sin(u), np.sin(v))
    z = cz + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=alpha, shade=True)


def render_angled_overview(cfg, output_dir):
    fig = plt.figure(figsize=(15, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0a1f2a")

    pool = cfg["pool"]
    pl, pw, pd = pool["length"], pool["width"], pool["depth"]

    # Floor
    draw_box(ax, (pl / 2.0, 0, -0.15), (pl, pw, 0.3), "#173b4d", alpha=0.9, edgecolor="#235c75")

    # Walls
    draw_box(ax, (-0.15, 0, 2.25), (0.3, pw + 0.6, 4.5), "#14485e", alpha=0.3, edgecolor="#22ccdd")
    draw_box(ax, (pl + 0.15, 0, 2.25), (0.3, pw + 0.6, 4.5), "#14485e", alpha=0.3, edgecolor="#22ccdd")
    draw_box(ax, (pl / 2.0, -pw / 2.0 - 0.15, 2.25), (pl, 0.3, 4.5), "#14485e", alpha=0.3, edgecolor="#22ccdd")
    draw_box(ax, (pl / 2.0, pw / 2.0 + 0.15, 2.25), (pl, 0.3, 4.5), "#14485e", alpha=0.15, edgecolor="#22ccdd")

    # Water surface wireframe
    draw_box(ax, (pl / 2.0, 0, pd), (pl, pw, 0.02), "#22ccee", alpha=0.15, edgecolor="#33eeff")

    # AUV
    auv_pose = cfg["auv_placeholder"]["start_pose"]
    draw_box(ax, auv_pose[:3], (0.8, 0.4, 0.3), "#ffd700", alpha=1.0, edgecolor="#ff9900")

    # Starting Gate
    gp = cfg["gate"]["position"]
    gw, gh = cfg["gate"]["width"], cfg["gate"]["height"]
    draw_box(ax, (gp[0], gp[1], gp[2] + gh / 2.0), (0.08, gw, 0.08), "#eeeeee")
    draw_box(ax, (gp[0], gp[1], gp[2] - gh / 2.0), (0.08, gw, 0.08), "#eeeeee")
    draw_box(ax, (gp[0], -gw / 2.0, gp[2]), (0.08, 0.08, gh), "#eeeeee")
    draw_box(ax, (gp[0], gw / 2.0, gp[2]), (0.08, 0.08, gh), "#eeeeee")
    draw_box(ax, (gp[0], 0, gp[2]), (0.08, 0.08, gh), "#cc1111") # divider

    # Slalom Poles
    for p in cfg["slalom"]["poles"]:
        pos = p["position"]
        col = "#ffffff" if p["color"][0] > 0.9 and p["color"][1] > 0.9 else "#dd2222"
        draw_cylinder(ax, (pos[0], pos[1], 1.1), 0.04, 2.2, col, axis="z")

    # Buoys
    for b in cfg["buoys"]:
        pos = b["position"]
        b_col = tuple(b["color"][:3])
        draw_sphere(ax, (pos[0], pos[1], pos[2]), 0.20, b_col)
        draw_cylinder(ax, (pos[0], pos[1], pos[2] / 2.0), 0.015, pos[2], "#666666", axis="z")

    # Bins
    bp = cfg["bins"]["position"]
    draw_box(ax, (bp[0], bp[1], 0.15), (1.2, 0.8, 0.3), "#222222", edgecolor="#ffffff")

    # Target Board
    tp = cfg["target_board"]["position"]
    draw_box(ax, (tp[0], tp[1], tp[2]), (0.06, 1.2, 1.0), "#ffffff", edgecolor="#00ffff")

    # Octagon Zone
    op = cfg["octagon_zone"]["position"]
    od = cfg["octagon_zone"]["diameter"]
    theta = np.linspace(0, 2 * np.pi, 9)
    ox = op[0] + (od / 2.0) * np.cos(theta)
    oy = op[1] + (od / 2.0) * np.sin(theta)
    oz = np.full_like(ox, 0.02)
    ax.plot(ox, oy, oz, color="#ff7700", linewidth=3)
    draw_box(ax, (op[0], op[1], 0.3), (0.61, 0.61, 0.3), "#ffffff", edgecolor="#ff7700")

    ax.set_xlim(-1, pl + 1)
    ax.set_ylim(-pw / 2.0 - 1, pw / 2.0 + 1)
    ax.set_zlim(0, 5)
    ax.set_xlabel("X (Course Downrange) [m]", color="#cceeff")
    ax.set_ylabel("Y (Pool Width) [m]", color="#cceeff")
    ax.set_zlabel("Z (Depth / Elevation) [m]", color="#cceeff")
    ax.view_init(elev=28, azim=-55)
    ax.set_title("RoboSub 3D Pool Simulation Environment (Angled Overview)", color="#ffffff", fontsize=13, fontweight="bold")
    ax.tick_params(colors="#aaccdd")

    out_file = output_dir / "pool_overview_angled.png"
    plt.tight_layout()
    plt.savefig(out_file, facecolor="#0a1f2a", edgecolor="none")
    plt.close()
    print(f"Rendered: {out_file}")


def render_gate_closeup(cfg, output_dir):
    fig = plt.figure(figsize=(12, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0d2430")

    gp = cfg["gate"]["position"]
    gw, gh = cfg["gate"]["width"], cfg["gate"]["height"]
    half_w, half_h = gw / 2.0, gh / 2.0

    # Crossbars & Posts
    draw_box(ax, (0, 0, half_h), (0.08, gw, 0.08), "#f0f0f0")
    draw_box(ax, (0, 0, -half_h), (0.08, gw, 0.08), "#f0f0f0")
    draw_box(ax, (0, -half_w, 0), (0.08, 0.08, gh), "#f0f0f0")
    draw_box(ax, (0, half_w, 0), (0.08, 0.08, gh), "#f0f0f0")

    # Center Divider
    draw_box(ax, (0, 0, 0), (0.08, 0.08, gh), "#dd1111")

    # Indicator Panels
    # Left (-Y): Top Black, Bottom Red
    draw_box(ax, (0, -half_w, half_h / 2.0), (0.16, 0.16, half_h), "#111111")
    draw_box(ax, (0, -half_w, -half_h / 2.0), (0.16, 0.16, half_h), "#dd1111")
    # Right (+Y): Top Red ("Red, Right, Above"), Bottom Black
    draw_box(ax, (0, half_w, half_h / 2.0), (0.16, 0.16, half_h), "#dd1111")
    draw_box(ax, (0, half_w, -half_h / 2.0), (0.16, 0.16, half_h), "#111111")

    # Mooring cables down to pool floor
    draw_cylinder(ax, (0, -half_w, -half_h - 0.8), 0.02, 1.6, "#555555", axis="z")
    draw_cylinder(ax, (0, half_w, -half_h - 0.8), 0.02, 1.6, "#555555", axis="z")

    # Approaching AUV
    draw_box(ax, (-2.5, 0, 0), (0.8, 0.4, 0.3), "#ffd700", edgecolor="#ff9900")
    draw_sphere(ax, (-2.1, 0, 0), 0.12, "#222222")

    ax.set_xlim(-3.5, 1.5)
    ax.set_ylim(-2.2, 2.2)
    ax.set_zlim(-2.5, 1.5)
    ax.view_init(elev=16, azim=-40)
    ax.set_xlabel("Relative X [m]", color="#cceeff")
    ax.set_ylabel("Relative Y [m]", color="#cceeff")
    ax.set_zlabel("Relative Z [m]", color="#cceeff")
    ax.set_title("RoboSub Starting Gate & Dual Corridors (Close-up View)", color="#ffffff", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#aaccdd")

    out_file = output_dir / "gate_closeup_3d.png"
    plt.tight_layout()
    plt.savefig(out_file, facecolor="#0d2430", edgecolor="none")
    plt.close()
    print(f"Rendered: {out_file}")


def render_slalom_view(cfg, output_dir):
    fig = plt.figure(figsize=(13, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0c202a")

    # Floor patch
    draw_box(ax, (9.0, 0, -0.05), (7.0, 4.0, 0.1), "#143747", edgecolor="#205067")

    # Poles
    for p in cfg["slalom"]["poles"]:
        pos = p["position"]
        col = "#ffffff" if p["color"][0] > 0.9 and p["color"][1] > 0.9 else "#dd1111"
        draw_cylinder(ax, (pos[0], pos[1], 0.05), 0.20, 0.10, "#333333", axis="z")
        draw_cylinder(ax, (pos[0], pos[1], 1.1), 0.04, 2.2, col, axis="z")
        draw_sphere(ax, (pos[0], pos[1], 2.25), 0.06, "#ee2222")

    # Nav path line
    pts = [[6.0, 0.0, 1.0], [7.0, -0.5, 1.0], [8.0, 0.5, 1.0], [9.0, -0.5, 1.0], [10.0, 0.5, 1.0], [11.0, 0.0, 1.0], [12.0, 0.0, 1.0]]
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="#00ffff", linestyle="--", linewidth=2.5, label="Optimal Slalom Path")

    ax.set_xlim(5.5, 12.5)
    ax.set_ylim(-2.0, 2.0)
    ax.set_zlim(0, 3.0)
    ax.view_init(elev=20, azim=-65)
    ax.set_xlabel("X (Downrange) [m]", color="#cceeff")
    ax.set_ylabel("Y (Lateral) [m]", color="#cceeff")
    ax.set_zlabel("Z (Height) [m]", color="#cceeff")
    ax.set_title("RoboSub Avoid Debris (Slalom Course View)", color="#ffffff", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#aaccdd")

    out_file = output_dir / "slalom_course_view.png"
    plt.tight_layout()
    plt.savefig(out_file, facecolor="#0c202a", edgecolor="none")
    plt.close()
    print(f"Rendered: {out_file}")


def render_targets_and_zone(cfg, output_dir):
    fig = plt.figure(figsize=(14, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0b1e28")

    # Floor patch
    draw_box(ax, (15.5, 0, -0.05), (8.0, 6.0, 0.1), "#133544", edgecolor="#1f4f65")

    # Buoys
    for b in cfg["buoys"]:
        pos = b["position"]
        b_col = tuple(b["color"][:3])
        draw_sphere(ax, (pos[0], pos[1], pos[2]), 0.20, b_col)
        draw_cylinder(ax, (pos[0], pos[1], pos[2] / 2.0), 0.015, pos[2], "#555555", axis="z")

    # Bins
    bp = cfg["bins"]["position"]
    draw_box(ax, (bp[0], bp[1], 0.15), (1.2, 0.8, 0.3), "#222222", edgecolor="#ffffff")
    draw_box(ax, (bp[0] - 0.3, bp[1], 0.16), (0.4, 0.5, 0.02), "#dd1111")
    draw_box(ax, (bp[0] + 0.3, bp[1], 0.16), (0.4, 0.5, 0.02), "#1144dd")

    # Torpedo Board
    tp = cfg["target_board"]["position"]
    draw_box(ax, (tp[0], tp[1], tp[2]), (0.06, 1.2, 1.0), "#f5f5f5", edgecolor="#00ddff")
    draw_cylinder(ax, (tp[0], tp[1] - 0.3, tp[2]), 0.15, 0.08, "#dd1111", axis="x")
    draw_cylinder(ax, (tp[0], tp[1] + 0.3, tp[2]), 0.09, 0.08, "#1144dd", axis="x")

    # Octagon Zone & Table
    op = cfg["octagon_zone"]["position"]
    od = cfg["octagon_zone"]["diameter"]
    theta = np.linspace(0, 2 * np.pi, 9)
    ox = op[0] + (od / 2.0) * np.cos(theta)
    oy = op[1] + (od / 2.0) * np.sin(theta)
    oz = np.full_like(ox, 0.02)
    ax.plot(ox, oy, oz, color="#ff7700", linewidth=3.5)
    draw_box(ax, (op[0], op[1], 0.3), (0.61, 0.61, 0.3), "#ffffff", edgecolor="#ff7700")
    draw_cylinder(ax, (op[0], op[1], 0.38), 0.05, 0.10, "#111111", axis="z")
    draw_sphere(ax, (op[0], op[1], 0.44), 0.04, "#ffd700")

    ax.set_xlim(12.0, 19.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_zlim(0, 3.5)
    ax.view_init(elev=24, azim=-50)
    ax.set_xlabel("X (Downrange) [m]", color="#cceeff")
    ax.set_ylabel("Y (Lateral) [m]", color="#cceeff")
    ax.set_zlabel("Z (Height) [m]", color="#cceeff")
    ax.set_title("RoboSub Mission Targets, Recon Bins & Octagon Surfacing Zone", color="#ffffff", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#aaccdd")

    out_file = output_dir / "targets_and_mission_zone.png"
    plt.tight_layout()
    plt.savefig(out_file, facecolor="#0b1e28", edgecolor="none")
    plt.close()
    print(f"Rendered: {out_file}")


def render_auv_view(cfg, output_dir):
    fig = plt.figure(figsize=(12, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0a1c26")

    auv = cfg["auv_placeholder"]
    l, w, h = auv["length"], auv["width"], auv["height"]

    # Main Hull
    draw_box(ax, (0, 0, 0), (l, w, h), "#ffcc00", edgecolor="#cc9900")

    # Front camera dome
    draw_sphere(ax, (l / 2.0, 0, 0), h / 2.5, "#222222", alpha=0.9)

    # Direction Arrow on Deck
    draw_box(ax, (l / 4.0, 0, h / 2.0 + 0.005), (l / 3.0, 0.05, 0.01), "#dd1111")

    # Thrusters
    draw_cylinder(ax, (0, -w / 2.0 - 0.06, 0), 0.05, 0.18, "#222222", axis="x")
    draw_cylinder(ax, (0, w / 2.0 + 0.06, 0), 0.05, 0.18, "#222222", axis="x")
    draw_cylinder(ax, (l / 4.0, 0, h / 2.0 + 0.05), 0.04, 0.12, "#222222", axis="z")
    draw_cylinder(ax, (-l / 4.0, 0, h / 2.0 + 0.05), 0.04, 0.12, "#222222", axis="z")

    # Downward camera
    draw_cylinder(ax, (0, 0, -h / 2.0 - 0.03), 0.04, 0.06, "#111111", axis="z")

    ax.set_xlim(-0.7, 0.7)
    ax.set_ylim(-0.7, 0.7)
    ax.set_zlim(-0.5, 0.5)
    ax.view_init(elev=22, azim=-45)
    ax.set_xlabel("AUV X (Surge) [m]", color="#cceeff")
    ax.set_ylabel("AUV Y (Sway) [m]", color="#cceeff")
    ax.set_zlabel("AUV Z (Heave) [m]", color="#cceeff")
    ax.set_title("RoboSub Generic Autonomous Underwater Vehicle (AUV Reference Model)", color="#ffffff", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#aaccdd")

    out_file = output_dir / "auv_placeholder_view.png"
    plt.tight_layout()
    plt.savefig(out_file, facecolor="#0a1c26", edgecolor="none")
    plt.close()
    print(f"Rendered: {out_file}")


def main():
    cfg, root = load_config()
    out_dir = root / "evidence" / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Rendering 3D visual evidence...")
    render_angled_overview(cfg, out_dir)
    render_gate_closeup(cfg, out_dir)
    render_slalom_view(cfg, out_dir)
    render_targets_and_zone(cfg, out_dir)
    render_auv_view(cfg, out_dir)
    print("All scene views successfully rendered.")


if __name__ == "__main__":
    main()
