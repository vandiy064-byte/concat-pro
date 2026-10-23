import os
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = ROOT_DIR / ".github" / "workflows"


class TestWindowsOnlyPipeline(unittest.TestCase):
    def test_release_workflow_has_no_phones_job(self):
        content = (WORKFLOWS_DIR / "release.yml").read_text(encoding="utf-8")
        self.assertNotIn("uses: ./.github/workflows/mobile.yml", content)
        self.assertNotIn("phones:", content)
        self.assertIn("needs: [check, build]", content)

    def test_mobile_workflow_has_no_push_trigger(self):
        content = (WORKFLOWS_DIR / "mobile.yml").read_text(encoding="utf-8")
        # Check that 'push:' is not under 'on:'
        lines = content.splitlines()
        on_block = []
        in_on = False
        for line in lines:
            if line.strip() == "on:":
                in_on = True
            elif in_on and line and not line.startswith(" ") and not line.startswith("\t"):
                in_on = False
            elif in_on:
                on_block.append(line)
        on_text = "\n".join(on_block)
        self.assertNotIn("push:", on_text)
        self.assertNotIn("pull_request:", on_text)
        self.assertIn("workflow_dispatch:", on_text)

    def test_nix_workflow_has_no_push_trigger(self):
        content = (WORKFLOWS_DIR / "nix.yml").read_text(encoding="utf-8")
        self.assertNotIn("push:", content)
        self.assertNotIn("pull_request:", content)
        self.assertIn("workflow_dispatch:", content)

    def test_ci_workflow_has_only_windows_desktop_job(self):
        content = (WORKFLOWS_DIR / "ci.yml").read_text(encoding="utf-8")
        self.assertNotIn("macos-15", content)
        self.assertIn("windows-2022", content)

    def test_build_app_matrix_contains_windows_target(self):
        content = (WORKFLOWS_DIR / "build-app.yml").read_text(encoding="utf-8")
        self.assertIn("platform: windows", content)
        self.assertIn("arch: x86_64", content)
        self.assertIn("os: windows-2022", content)
        self.assertIn("Publish to GitHub Releases", content)


if __name__ == "__main__":
    unittest.main()
