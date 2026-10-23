"""
Unit tests for CI compilation and timeout optimization.
Validates that .github/workflows/ci.yml parallelizes build jobs and sets
sufficient timeouts to avoid GitHub Actions timeout failures.
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

    def test_engine_job_timeout(self):
        engine = self.data["jobs"]["engine"]
        self.assertGreaterEqual(
            engine.get("timeout-minutes", 0),
            150,
            "Engine job overall timeout should be at least 150 minutes",
        )

    def test_no_single_thread_bottlenecks(self):
        self.assertNotIn(
            "--build-jobs 1",
            self.content,
            "Found --build-jobs 1 in ci.yml which causes 25m timeout failure",
        )
        self.assertNotIn(
            "-j 1",
            self.content,
            "Found -j 1 in ci.yml which slows down doc testing",
        )

    def test_build_the_tests_step(self):
        steps = self.data["jobs"]["engine"]["steps"]
        build_step = next((s for s in steps if s.get("name") == "Build the tests"), None)
        self.assertIsNotNone(build_step, "Step 'Build the tests' not found")
        self.assertGreaterEqual(
            build_step.get("timeout-minutes", 0),
            50,
            "Build the tests timeout should be at least 50 minutes",
        )
        self.assertIn(
            "--build-jobs 2",
            build_step.get("run", ""),
            "Build the tests should compile with 2 parallel jobs",
        )

    def test_run_the_tests_step(self):
        steps = self.data["jobs"]["engine"]["steps"]
        test_step = next((s for s in steps if s.get("name") == "Run the tests"), None)
        self.assertIsNotNone(test_step, "Step 'Run the tests' not found")
        self.assertGreaterEqual(
            test_step.get("timeout-minutes", 0),
            35,
            "Run the tests timeout should be at least 35 minutes",
        )
        self.assertIn(
            "--build-jobs 2",
            test_step.get("run", ""),
            "Run the tests should execute with 2 parallel jobs",
        )


if __name__ == "__main__":
    unittest.main()
