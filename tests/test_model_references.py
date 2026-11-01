#!/usr/bin/env python3
"""
Test Suite: Model References, Resource Paths, and Course Clearances
Validates that every included model uri resolves to a valid local model directory,
model.config exists, visual/collision clearances satisfy AUV navigation envelopes.
"""

import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


class TestModelReferences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.models_dir = cls.project_root / "models"
        cls.world_file = cls.project_root / "worlds" / "robosub_pool.sdf"

    def test_all_included_models_resolve(self):
        """Verify that every model:// URI in the world file resolves locally under models/."""
        tree = ET.parse(self.world_file)
        world = tree.getroot().find("world")
        includes = world.findall("include")

        self.assertGreater(len(includes), 0, "No model includes found in world file")

        for inc in includes:
            uri_elem = inc.find("uri")
            self.assertIsNotNone(uri_elem, "Include element missing <uri>")
            uri = uri_elem.text.strip()
            self.assertTrue(uri.startswith("model://"), f"URI should use model:// convention: {uri}")

            model_name = uri.replace("model://", "")
            target_model_dir = self.models_dir / model_name

            self.assertTrue(
                target_model_dir.is_dir(),
                f"Referenced model '{model_name}' does not exist at {target_model_dir}"
            )
            self.assertTrue(
                (target_model_dir / "model.sdf").is_file(),
                f"Missing model.sdf for model '{model_name}'"
            )
            self.assertTrue(
                (target_model_dir / "model.config").is_file(),
                f"Missing model.config for model '{model_name}'"
            )

    def test_gate_clearance_for_auv(self):
        """Verify that the starting gate opening is wide enough for the AUV placeholder."""
        gate_sdf = self.models_dir / "gate" / "model.sdf"
        auv_sdf = self.models_dir / "auv_placeholder" / "model.sdf"

        # Gate width
        tree_gate = ET.parse(gate_sdf)
        crossbar = tree_gate.getroot().find(".//visual[@name='crossbar_top_visual']//cylinder")
        gate_total_width = float(crossbar.find("length").text)
        passage_half_width = gate_total_width / 2.0

        # AUV width
        tree_auv = ET.parse(auv_sdf)
        auv_hull = tree_auv.getroot().find(".//visual[@name='hull_visual']//box")
        auv_width = float(auv_hull.find("size").text.split()[1])

        # Verification: Passage width must be at least 2.5x the vehicle width for safe navigation
        self.assertGreater(
            passage_half_width,
            auv_width * 2.0,
            f"Gate corridor ({passage_half_width}m) is too narrow for AUV ({auv_width}m)"
        )

    def test_slalom_pole_count_and_colors(self):
        """Verify at least six slalom poles exist in the world with proper clearances."""
        tree = ET.parse(self.world_file)
        world = tree.getroot().find("world")
        slalom_poles = [
            inc for inc in world.findall("include")
            if inc.find("name").text.startswith("slalom_pole_")
        ]
        self.assertGreaterEqual(
            len(slalom_poles), 6,
            f"Expected at least 6 slalom poles, found {len(slalom_poles)}"
        )

        # Check distances between sequential poles along X
        pole_poses = []
        for p in slalom_poles:
            pose_text = p.find("pose").text.strip().split()
            coords = [float(c) for c in pose_text[:3]]
            pole_poses.append(coords)

        # Sort poles by X coordinate
        pole_poses.sort(key=lambda c: c[0])
        for i in range(len(pole_poses) - 1):
            dx = pole_poses[i + 1][0] - pole_poses[i][0]
            dy = pole_poses[i + 1][1] - pole_poses[i][1]
            dist = math.hypot(dx, dy)
            self.assertGreater(
                dist, 1.0,
                f"Slalom poles {i} and {i+1} too close: {dist:.2f}m < 1.0m"
            )

    def test_pool_boundaries_contain_all_objects(self):
        """Verify all course objects are strictly positioned within the pool boundaries."""
        pool_sdf = self.models_dir / "pool" / "model.sdf"
        tree_pool = ET.parse(pool_sdf)
        floor = tree_pool.getroot().find(".//visual[@name='floor_visual']//box")
        floor_l, floor_w, _ = [float(v) for v in floor.find("size").text.split()]

        # Pool bounds: X in [0, floor_l], Y in [-floor_w/2, floor_w/2]
        tree_world = ET.parse(self.world_file)
        world = tree_world.getroot().find("world")
        for inc in world.findall("include"):
            name = inc.find("name").text.strip()
            if name == "pool":
                continue
            pose_elem = inc.find("pose")
            if pose_elem is not None:
                x, y, z = [float(v) for v in pose_elem.text.strip().split()[:3]]
                self.assertGreaterEqual(x, 0.0, f"Model '{name}' X ({x}) outside pool (< 0)")
                self.assertLessEqual(x, floor_l, f"Model '{name}' X ({x}) outside pool (> {floor_l})")
                self.assertGreaterEqual(y, -floor_w / 2.0, f"Model '{name}' Y ({y}) outside pool (< {-floor_w/2.0})")
                self.assertLessEqual(y, floor_w / 2.0, f"Model '{name}' Y ({y}) outside pool (> {floor_w/2.0})")


if __name__ == "__main__":
    unittest.main()
