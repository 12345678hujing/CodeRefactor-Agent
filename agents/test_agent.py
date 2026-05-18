"""Test agent - runs test suites and generates missing tests."""
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional


class TestAgent:
    """Runs tests, validates refactored code, and generates missing test cases."""

    def __init__(self, test_command: str = "pytest", coverage: bool = True):
        self.test_command = test_command
        self.coverage = coverage
        self.results: List[Dict[str, Any]] = []

    def run_tests(self, target: Path, args: List[str] = None) -> Dict[str, Any]:
        """Execute test suite and return results."""
        args = args or ["-v", "--tb=short"]
        cmd = [self.test_command, str(target)] + args
        if self.coverage:
            cmd = ["coverage", "run", "-m"] + cmd

        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )
            result = {
                "success": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "test_count": self._parse_test_count(proc.stdout),
                "failed": self._parse_failures(proc.stdout)
            }
        except subprocess.TimeoutExpired:
            result = {"success": False, "error": "timeout"}
        except FileNotFoundError:
            result = {"success": False, "error": f"{self.test_command} not found"}

        self.results.append(result)
        return result

    def generate_missing_tests(self, source_file: Path, coverage_data: Dict) -> List[Dict]:
        """Identify uncovered code paths and suggest test cases."""
        suggestions = []
        uncovered = coverage_data.get("missing_lines", [])
        for line_no in uncovered[:20]:
            suggestions.append({
                "file": str(source_file),
                "line": line_no,
                "status": "pending",
                "suggestion": f"Add test for uncovered line {line_no}"
            })
        return suggestions

    def _parse_test_count(self, output: str) -> int:
        """Extract test count from pytest output."""
        import re
        match = re.search(r"collected (\d+) items", output)
        return int(match.group(1)) if match else 0

    def _parse_failures(self, output: str) -> List[str]:
        """Extract failed test names from pytest output."""
        failures = []
        for line in output.split("\n"):
            if "FAILED" in line:
                failures.append(line.strip())
        return failures

    def coverage_report(self) -> Optional[Dict[str, Any]]:
        """Generate coverage summary if coverage data available."""
        try:
            proc = subprocess.run(
                ["coverage", "report", "--format=json"],
                capture_output=True, text=True, timeout=30
            )
            import json
            return json.loads(proc.stdout) if proc.returncode == 0 else None
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def __repr__(self):
        return f"TestAgent(command={self.test_command}, coverage={self.coverage})"
