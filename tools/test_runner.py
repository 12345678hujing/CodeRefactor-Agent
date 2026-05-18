"""Test runner wrapper - discovers and executes test suites."""
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional


class TestRunner:
    """Discovers and runs tests, returns structured results."""

    def __init__(self, default_timeout: int = 300):
        self.default_timeout = default_timeout

    def run_pytest(self, target: Path, args: List[str] = None) -> Dict[str, Any]:
        """Run pytest on target directory/file."""
        args = args or ["-v", "--tb=short", "--no-header"]
        cmd = ["python", "-m", "pytest", str(target)] + args
        return self._execute(cmd)

    def run_unittest(self, target: Path) -> Dict[str, Any]:
        """Run unittest discover on target directory."""
        cmd = ["python", "-m", "unittest", "discover", "-s", str(target), "-v"]
        return self._execute(cmd)

    def collect_tests(self, target: Path) -> List[str]:
        """List all test files in target directory."""
        test_files = []
        for pattern in ["**/test_*.py", "**/*_test.py", "**/test_*.ts", "**/*.test.ts"]:
            test_files.extend(str(f) for f in target.rglob(pattern))
        return sorted(test_files)

    def _execute(self, cmd: List[str]) -> Dict[str, Any]:
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=self.default_timeout
            )
            return {
                "success": proc.returncode == 0,
                "returncode": proc.returncode,
                "stdout": proc.stdout[-2000:] if len(proc.stdout) > 2000 else proc.stdout,
                "stderr": proc.stderr[-1000:] if len(proc.stderr) > 1000 else proc.stderr,
                "command": " ".join(cmd)
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "timeout", "command": " ".join(cmd)}
        except FileNotFoundError:
            return {"success": False, "error": "python not found", "command": " ".join(cmd)}

    def __repr__(self):
        return f"TestRunner(timeout={self.default_timeout})"
