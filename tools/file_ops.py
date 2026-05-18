"""File operations for reading, writing, and searching code files."""
import re
from pathlib import Path
from typing import List, Optional


class FileOperator:
    """Handles file I/O operations with safety guards."""

    ALLOWED_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java",
                         ".go", ".rs", ".c", ".cpp", ".h", ".hpp",
                         ".md", ".yaml", ".yml", ".json", ".toml",
                         ".cfg", ".ini", ".txt", ".csv", ".sql"}

    def __init__(self, max_file_size: int = 1_000_000):
        self.max_file_size = max_file_size

    def read_file(self, path: Path) -> Optional[str]:
        """Read file content with size and extension checks."""
        if not self._validate(path):
            return None
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except (IOError, PermissionError):
            return None

    def write_file(self, path: Path, content: str) -> bool:
        """Write content to file. Creates parent dirs if needed."""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except (IOError, PermissionError):
            return False

    def search_files(self, directory: Path, pattern: str,
                     glob_pattern: str = "**/*.py") -> List[dict]:
        """Search for regex pattern in files matching glob."""
        results = []
        compiled = re.compile(pattern)
        for file_path in directory.rglob(glob_pattern):
            if "site-packages" in str(file_path) or "__pycache__" in str(file_path):
                continue
            content = self.read_file(file_path)
            if content is None:
                continue
            for i, line in enumerate(content.split("\n"), 1):
                if compiled.search(line):
                    results.append({
                        "file": str(file_path),
                        "line": i,
                        "content": line.strip()
                    })
        return results

    def _validate(self, path: Path) -> bool:
        """Validate file can be read (extension, size, existence)."""
        if not path.exists():
            return False
        if path.suffix not in self.ALLOWED_EXTENSIONS:
            return False
        if path.stat().st_size > self.max_file_size:
            return False
        return True

    def __repr__(self):
        return f"FileOperator(max_size={self.max_file_size})"
