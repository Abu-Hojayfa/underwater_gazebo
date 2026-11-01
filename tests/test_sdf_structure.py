#!/usr/bin/env python3
"""
Test Suite: SDFormat Structure and Syntax Validation
Validates XML syntax, SDF version tags, required Gazebo world elements,
model links, visual/collision geometries, and non-empty dimension attributes.
"""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


class TestSDFStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.worlds_dir = cls.project_root / "worlds"
        cls.models_dir = cls.project_root / "models"
        cls.world_file = cls.worlds_dir / "robosub_pool.sdf"

    def test_world_file_exists(self):
        """Verify the main world SDF file exists on disk."""
        self.assertTrue(self.world_file.exists(), f"World file not found: {self.world_file}")

    def test_world_xml_well_formed(self):
        """Verify that the world file is valid, parseable XML."""
        try:
            tree = ET.parse(self.world_file)
            root = tree.getroot()
        except ET.ParseError as e:
            self.fail(f"XML parse error in {self.world_file}: {e}")

        self.assertEqual(root.tag, "sdf", "Root element must be <sdf>")
        version = root.attrib.get("version")
        self.assertIsNotNone(version, "Root <sdf> must contain a version attribute")
        self.assertIn(version, ["1.8", "1.9", "1.10"], f"Unexpected SDF version: {version}")

    def test_world_required_elements(self):
        """Verify that required world children exist: world, physics, scene, light."""
        tree = ET.parse(self.world_file)
        root = tree.getroot()
        world = root.find("world")
        self.assertIsNotNone(world, "Missing <world> element under root <sdf>")
        self.assertTrue(world.attrib.get("name"), "World element must have a non-empty 'name' attribute")

        # Physics
        physics = world.find("physics")
        self.assertIsNotNone(physics, "Missing <physics> configuration in world")
        max_step = physics.find("max_step_size")
        self.assertIsNotNone(max_step, "Missing <max_step_size> in physics")
        self.assertGreater(float(max_step.text), 0, "max_step_size must be positive")

        # Scene
        scene = world.find("scene")
        self.assertIsNotNone(scene, "Missing <scene> element in world")
        ambient = scene.find("ambient")
        self.assertIsNotNone(ambient, "Missing <ambient> light in scene")
        background = scene.find("background")
        self.assertIsNotNone(background, "Missing <background> color in scene")

        # Light
        lights = world.findall("light")
        self.assertGreaterEqual(len(lights), 1, "At least one <light> must be configured")

        # Plugins
        plugins = world.findall("plugin")
        self.assertGreaterEqual(len(plugins), 3, "Core systems (physics, user commands, scene broadcaster) required")
        plugin_names = [p.attrib.get("filename") for p in plugins]
        self.assertIn("gz-sim-physics-system", plugin_names)
        self.assertIn("gz-sim-scene-broadcaster-system", plugin_names)

    def test_all_models_xml_valid(self):
        """Verify every model.sdf in the models/ tree is valid XML with link and visual elements."""
        model_sdf_files = list(self.models_dir.glob("*/model.sdf"))
        self.assertGreater(len(model_sdf_files), 0, "No model.sdf files found in models directory")

        for sdf_path in model_sdf_files:
            with self.subTest(model_path=str(sdf_path)):
                try:
                    tree = ET.parse(sdf_path)
                    root = tree.getroot()
                except ET.ParseError as e:
                    self.fail(f"Invalid XML in {sdf_path}: {e}")

                self.assertEqual(root.tag, "sdf")
                model = root.find("model")
                self.assertIsNotNone(model, f"Missing <model> in {sdf_path}")
                self.assertTrue(model.attrib.get("name"), f"Model in {sdf_path} lacks a name")

                links = model.findall("link")
                self.assertGreaterEqual(len(links), 1, f"Model {sdf_path} has no <link> elements")

                for link in links:
                    visuals = link.findall("visual")
                    collisions = link.findall("collision")
                    # Every link must have at least one visual or collision
                    self.assertGreater(len(visuals) + len(collisions), 0, f"Link in {sdf_path} is empty")

                    # Check collision geometry validity
                    for col in collisions:
                        geom = col.find("geometry")
                        self.assertIsNotNone(geom, f"Collision in {sdf_path} missing <geometry>")
                        # Ensure sizes/radii are positive
                        box = geom.find("box")
                        if box is not None:
                            size = box.find("size").text.strip().split()
                            self.assertEqual(len(size), 3)
                            self.assertTrue(all(float(v) > 0 for v in size))

                        cylinder = geom.find("cylinder")
                        if cylinder is not None:
                            rad = float(cylinder.find("radius").text.strip())
                            length = float(cylinder.find("length").text.strip())
                            self.assertGreater(rad, 0)
                            self.assertGreater(length, 0)

                        sphere = geom.find("sphere")
                        if sphere is not None:
                            rad = float(sphere.find("radius").text.strip())
                            self.assertGreater(rad, 0)

    def test_no_duplicate_model_names_in_world(self):
        """Ensure no duplicate names exist among top-level included entities in the world."""
        tree = ET.parse(self.world_file)
        world = tree.getroot().find("world")
        names = []
        for inc in world.findall("include"):
            name = inc.find("name")
            if name is not None and name.text:
                names.append(name.text.strip())

        self.assertEqual(len(names), len(set(names)), f"Duplicate model names found in world: {names}")


if __name__ == "__main__":
    unittest.main()
