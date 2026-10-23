"""
Unit tests for the Concat Pro auto-release and manifest pipeline.
Validates that release manifests conform to what concat-host/src/updates.rs expects
for in-app updates.
"""
import importlib.util
import json
import os
import pathlib
import subprocess
import unittest

def find_repo_root() -> pathlib.Path:
    cur = pathlib.Path(__file__).resolve().parent
    if (cur / "src" / "Cargo.toml").exists():
        return cur
    if (cur.parent / "src" / "Cargo.toml").exists():
        return cur.parent
    if (cur.parent / "Concat-main" / "src" / "Cargo.toml").exists():
        return cur.parent / "Concat-main"
    return cur

ROOT = find_repo_root()

class TestReleasePipeline(unittest.TestCase):
    def test_models_repo_default(self):
        # Verify models.py uses vandiy064-byte/concat-pro
        models_path = ROOT / "scripts" / "models.py"
        spec = importlib.util.spec_from_file_location("concat_models_script", str(models_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.REPO, "vandiy064-byte/concat-pro")

    def test_release_manifest_generation(self):
        out_file = ROOT / "test_manifest.json"
        try:
            res = subprocess.run(
                ["python", str(ROOT / "scripts" / "models.py"), "release-manifest",
                 "--version", "2.0.12", "--tag", "v2.0.12", "--out", str(out_file)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(res.returncode, 0, f"models.py failed: {res.stderr}")
            self.assertTrue(out_file.exists(), "Manifest file was not created")

            with open(out_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["version"], "2.0.12")
            self.assertEqual(data["tag"], "v2.0.12")
            self.assertEqual(data["product"], "Concat")
            self.assertIn("binaries", data)
            self.assertIn("windows", data["binaries"])
            self.assertIn("x86_64", data["binaries"]["windows"])

            win_setup = data["binaries"]["windows"]["x86_64"]["setup"]
            self.assertEqual(win_setup["file"], "Concat-2.0.12-windows-x86_64-setup.exe")
            expected_url = "https://github.com/vandiy064-byte/concat-pro/releases/download/v2.0.12/Concat-2.0.12-windows-x86_64-setup.exe"
            self.assertEqual(win_setup["url"], expected_url)

        finally:
            if out_file.exists():
                out_file.unlink()

    def test_cargo_toml_version(self):
        cargo_toml = (ROOT / "src" / "Cargo.toml").read_text(encoding="utf-8")
        self.assertIn('version = "2.0.12"', cargo_toml, "Cargo.toml version should be 2.0.12")

if __name__ == "__main__":
    unittest.main()
