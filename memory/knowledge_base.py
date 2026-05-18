"""Knowledge base for project-specific rules, patterns, and best practices."""
from typing import List, Dict, Any, Optional


class KnowledgeBase:
    """Stores and retrieves project-specific knowledge: coding standards,
    architecture decisions, and recurring patterns."""

    def __init__(self):
        self._rules: List[Dict[str, Any]] = []
        self._patterns: List[Dict[str, Any]] = []

    def add_rule(self, name: str, description: str, category: str = "general") -> str:
        """Register a project rule or coding standard."""
        import uuid
        rule_id = str(uuid.uuid4())[:8]
        self._rules.append({
            "id": rule_id,
            "name": name,
            "description": description,
            "category": category
        })
        return rule_id

    def add_pattern(self, name: str, code_snippet: str, language: str = "python") -> str:
        """Register a reusable code pattern."""
        import uuid
        pattern_id = str(uuid.uuid4())[:8]
        self._patterns.append({
            "id": pattern_id,
            "name": name,
            "code": code_snippet,
            "language": language
        })
        return pattern_id

    def get_rules(self, category: Optional[str] = None) -> List[Dict]:
        """Retrieve rules, optionally filtered by category."""
        if category:
            return [r for r in self._rules if r["category"] == category]
        return self._rules

    def search_patterns(self, query: str) -> List[Dict]:
        """Search patterns by keyword."""
        q = query.lower()
        return [p for p in self._patterns if q in p["name"].lower() or q in p["code"].lower()]

    def load_defaults(self):
        """Load default coding standards."""
        self.add_rule(
            "naming_convention",
            "Use snake_case for functions/variables, PascalCase for classes",
            "style"
        )
        self.add_rule(
            "type_hints",
            "All public functions must have type annotations",
            "style"
        )
        self.add_rule(
            "error_handling",
            "Never use bare except: always specify exception types",
            "safety"
        )
        self.add_rule(
            "test_coverage",
            "New code must maintain minimum 80% test coverage",
            "testing"
        )
        self.add_pattern(
            "repository_pattern",
            "class Repository:\n    def __init__(self, db):\n        self.db = db\n    def get(self, id): ...",
            "python"
        )

    def __repr__(self):
        return f"KnowledgeBase(rules={len(self._rules)}, patterns={len(self._patterns)})"
