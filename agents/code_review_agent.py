"""Code review agent - analyzes code for issues, anti-patterns, and security flaws."""
import re
from pathlib import Path
from typing import List, Dict, Any


class CodeReviewAgent:
    """Analyzes source code for quality issues, security vulnerabilities,
    and violations of coding standards."""

    def __init__(self, model: str = "claude-sonnet-4-20250514", memory_client=None):
        self.model = model
        self.memory = memory_client
        self.issues: List[Dict[str, Any]] = []

    def scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan a single file for issues."""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        file_issues = []

        file_issues.extend(self._check_long_functions(file_path, lines))
        file_issues.extend(self._check_broad_exceptions(file_path, lines))
        file_issues.extend(self._check_sql_injection(file_path, lines))
        file_issues.extend(self._check_todos(file_path, lines))
        file_issues.extend(self._check_duplicate_code(file_path, lines))

        return file_issues

    def scan_directory(self, directory: Path, pattern: str = "**/*.py") -> List[Dict[str, Any]]:
        """Recursively scan a directory for issues."""
        all_issues = []
        for file_path in sorted(directory.rglob(pattern)):
            if "site-packages" in str(file_path) or "__pycache__" in str(file_path):
                continue
            issues = self.scan_file(file_path)
            all_issues.extend(issues)
        return all_issues

    def _check_long_functions(self, file_path: Path, lines: List[str]) -> List[Dict]:
        issues = []
        threshold = 80
        func_start = None
        for i, line in enumerate(lines):
            if re.match(r"^\s*def \w+", line) or re.match(r"^\s*class \w+", line):
                if func_start is not None and i - func_start > threshold:
                    name = lines[func_start].strip()
                    issues.append({
                        "severity": "medium",
                        "type": "long_function",
                        "file": str(file_path),
                        "line": func_start + 1,
                        "message": f"Function/class too long: {name} ({i - func_start} lines)",
                        "suggestion": "Consider splitting into smaller functions"
                    })
                func_start = i
        return issues

    def _check_broad_exceptions(self, file_path: Path, lines: List[str]) -> List[Dict]:
        issues = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped == "except:" or "except Exception as" in stripped:
                issues.append({
                    "severity": "critical",
                    "type": "broad_exception",
                    "file": str(file_path),
                    "line": i,
                    "message": f"Broad exception clause: {stripped}",
                    "suggestion": "Catch specific exceptions instead"
                })
        return issues

    def _check_sql_injection(self, file_path: Path, lines: List[str]) -> List[Dict]:
        issues = []
        for i, line in enumerate(lines, 1):
            if re.search(r'f["\'].*(?:SELECT|INSERT|DELETE|UPDATE)', line, re.IGNORECASE):
                issues.append({
                    "severity": "critical",
                    "type": "sql_injection",
                    "file": str(file_path),
                    "line": i,
                    "message": f"Potential SQL injection via f-string: {line.strip()}",
                    "suggestion": "Use parameterized queries (? placeholders)"
                })
        return issues

    def _check_todos(self, file_path: Path, lines: List[str]) -> List[Dict]:
        issues = []
        for i, line in enumerate(lines, 1):
            if re.search(r"TODO|FIXME|HACK|XXX", line, re.IGNORECASE):
                issues.append({
                    "severity": "suggestion",
                    "type": "todo",
                    "file": str(file_path),
                    "line": i,
                    "message": f"Unresolved marker: {line.strip()}",
                    "suggestion": "Address or remove before production"
                })
        return issues

    def _check_duplicate_code(self, file_path: Path, lines: List[str]) -> List[Dict]:
        issues = []
        block_sigs = {}
        for i, line in enumerate(lines):
            stripped = line.strip()
            if len(stripped) > 30 and not stripped.startswith(("#", "import", "from", "//", "/*")):
                sig = hash(stripped)
                block_sigs.setdefault(sig, []).append(i)
        for sig, positions in block_sigs.items():
            if len(positions) > 3:
                issues.append({
                    "severity": "medium",
                    "type": "duplicate_code",
                    "file": str(file_path),
                    "line": positions[0] + 1,
                    "message": f"Duplicate code block (appears {len(positions)} times at lines {[p+1 for p in positions[:5]]})",
                    "suggestion": "Extract into a shared function"
                })
        return issues

    def generate_report(self, issues: List[Dict]) -> Dict[str, Any]:
        """Group issues by severity and generate summary."""
        report = {"critical": [], "medium": [], "suggestion": [], "total": len(issues)}
        for issue in issues:
            report[issue["severity"]].append(issue)
        return report

    def __repr__(self):
        return f"CodeReviewAgent(model={self.model})"
