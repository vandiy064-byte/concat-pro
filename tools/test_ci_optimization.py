"""
Unit tests for CI pipeline optimization and Windows release stabilization.
Validates that .github/workflows/ci.yml:
1. Focuses Linux engine job on static analysis, linting, and clippy verification.
2. Avoids fragile Linux GUI test compilation bottlenecks.
3. Authoritatively executes full nextest and export tests on Windows (windows-2022).
"""
import unittest
from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CI_WORKFLOW = ROOT_DIR / ".github" / "workflows" / "ci.yml"


class TestCIOptimization(unittest.TestCase):
    def setUp(self):
        self.content = CI_WORKFLOW.read_text(encoding="utf-8")
        self.data = yaml.safe_load(self.content)

    def test_yaml_syntax_valid(self):
        self.assertIsInstance(self.data, dict)
        self.assertIn("jobs", self.data)
        self.assertIn("engine", self.data["jobs"])
        self.assertIn("desktop", self.data["jobs"])

    def test_engine_job_lints_present(self):
        steps = self.data["jobs"]["engine"]["steps"]
        step_runs = [s.get("run", "") for s in steps]
        all_runs = "\n".join(step_runs)
        self.assertIn("cargo fmt --check", all_runs)
        self.assertIn("scripts/locales.py --check", all_runs)
        self.assertIn("scripts/models.py --check", all_runs)
        self.assertIn("cargo clippy --workspace --all-targets -- -D warnings", all_runs)

    def test_no_fragile_linux_test_compilation(self):
        # Linux engine job should not build nextest GUI tests which cause OOM 143 or 25m timeout
        engine_steps = self.data["jobs"]["engine"]["steps"]
        for s in engine_steps:
            self.assertNotEqual(s.get("name"), "Build the tests")
            self.assertNotEqual(s.get("name"), "Run the tests")

    def test_windows_desktop_tests_intact(self):
        desktop_steps = self.data["jobs"]["desktop"]["steps"]
        build_step = next(
            (s for s in desktop_steps if s.get("name") == "Build the tests (Windows)"),
            None,
        )
        self.assertIsNotNone(build_step)
        self.assertIn("--build-jobs 2", build_step.get("run", ""))

        run_step = next(
            (s for s in desktop_steps if s.get("name") == "Run the tests (Windows)"),
            None,
        )
        self.assertIsNotNone(run_step)
        self.assertIn("--build-jobs 2", run_step.get("run", ""))


if __name__ == "__main__":
    unittest.main()
