"""Orchestrator agent - task routing, state management, and agent coordination."""
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents import CodeReviewAgent, RefactorAgent, TestAgent, SummaryAgent
from memory import VectorStore
from tools.git_ops import GitOperator
from tools.file_ops import FileOperator
from tools.test_runner import TestRunner


class OrchestratorAgent:
    """Central supervisor that coordinates specialized agents and manages task lifecycle."""

    def __init__(self, workspace: str = ".", model: str = "claude-sonnet-4-20250514"):
        self.workspace = Path(workspace)
        self.model = model
        self.session_id = str(uuid.uuid4())[:8]
        self.memory = VectorStore(persist_dir=str(self.workspace / ".memory"))
        self.git = GitOperator(workspace)
        self.file_ops = FileOperator()
        self.test_runner = TestRunner()

        self.code_reviewer = CodeReviewAgent(model=model, memory_client=self.memory)
        self.refactorer = RefactorAgent(model=model)
        self.tester = TestAgent()
        self.summarizer = SummaryAgent()

        self.task_log: List[Dict] = []
        self.context: Dict[str, Any] = {}

    def run_pipeline(self, task_type: str, target: str, **kwargs) -> Dict[str, Any]:
        """Execute full pipeline: review → (refactor) → test → summary."""
        target_path = self.workspace / target
        self._log("receive", f"task={task_type} target={target}")

        # Phase 1: Code Review
        self._log("phase", "starting CodeReviewAgent")
        issues = self.code_reviewer.scan_directory(target_path)
        review_report = self.code_reviewer.generate_report(issues)
        self._log("complete", f"CodeReview: {review_report['total']} issues found")

        # Phase 2: Refactor (optional)
        refactor_result = {"changes": [], "summary": {}}
        if kwargs.get("auto_refactor", True) and issues:
            self._log("phase", "starting RefactorAgent")
            for issue in issues:
                fp = Path(issue["file"])
                if fp.exists():
                    self.refactorer.apply_refactoring(fp, [issue])
            refactor_result = self.refactorer.summary()
            self._log("complete", f"Refactor: {refactor_result['total_changes']} changes")

        # Phase 3: Test
        self._log("phase", "starting TestAgent")
        test_result = self.tester.run_tests(target_path)
        if not test_result.get("success", False):
            missing_tests = self.tester.generate_missing_tests(
                target_path / "main.py", {"missing_lines": []}
            )
            test_result["missing_tests"] = missing_tests
        self._log("complete", f"Test: {test_result.get('test_count', 0)} tests")

        # Phase 4: Summary
        self._log("phase", "starting SummaryAgent")
        report = self.summarizer.generate_report(
            {"issues": issues}, refactor_result, test_result
        )
        pr_description = self.summarizer.generate_pr_description(report)

        pipeline_result = {
            "session_id": self.session_id,
            "task": task_type,
            "target": target,
            "completed_at": datetime.now().isoformat(),
            "review": review_report,
            "refactor": refactor_result,
            "test": test_result,
            "report": report,
            "pr_description": pr_description
        }

        self._log("complete", "pipeline finished")
        return pipeline_result

    def run_review_only(self, target: str) -> Dict[str, Any]:
        """Run code review only, without refactoring."""
        target_path = self.workspace / target
        self.context["mode"] = "review_only"
        issues = self.code_reviewer.scan_directory(target_path)
        report = self.code_reviewer.generate_report(issues)
        return {"issues": issues, "report": report}

    def _log(self, event: str, message: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "message": message
        }
        self.task_log.append(entry)

    def get_history(self) -> List[Dict]:
        """Return full task execution history for this session."""
        return self.task_log

    def reset(self):
        """Reset session state, clear context and task log."""
        self.session_id = str(uuid.uuid4())[:8]
        self.task_log.clear()
        self.context.clear()

    def __repr__(self):
        return f"OrchestratorAgent(session={self.session_id}, model={self.model})"
