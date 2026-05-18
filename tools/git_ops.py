"""Git operations wrapper for repository interactions."""
import subprocess
from pathlib import Path
from typing import List, Optional


class GitOperator:
    """Wrapper around git CLI for repository operations."""

    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)

    def diff(self, base: str = "HEAD", staged: bool = False) -> str:
        """Get git diff output."""
        cmd = ["git", "diff"]
        if staged:
            cmd.append("--cached")
        cmd.append(base)
        return self._run(cmd)

    def log(self, max_count: int = 10, format: str = "%h %s") -> str:
        """Get recent commit log."""
        return self._run([
            "git", "log", f"--max-count={max_count}",
            f"--pretty=format:{format}"
        ])

    def branch(self) -> str:
        """Get current branch name."""
        return self._run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()

    def changed_files(self, base: str = "HEAD") -> List[str]:
        """List files changed in working tree vs base."""
        out = self._run(["git", "diff", "--name-only", base])
        return [f.strip() for f in out.split("\n") if f.strip()]

    def commit(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Stage files and create a commit."""
        if files:
            self._run(["git", "add"] + files)
        else:
            self._run(["git", "add", "-A"])
        result = self._run(["git", "commit", "-m", message])
        return result.strip() != ""

    def create_branch(self, name: str, base: str = "main") -> bool:
        """Create and switch to a new branch."""
        self._run(["git", "checkout", "-b", name, base])
        return True

    def _run(self, cmd: List[str]) -> str:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True,
                cwd=str(self.workspace)
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"error: {e.stderr}"

    def __repr__(self):
        branch = self.branch()[:20] if hasattr(self, 'branch') else "?"
        return f"GitOperator(workspace={self.workspace}, branch={branch})"
