"""Static analysis utilities for Python source code.

This module deliberately does not execute analyzed source code.
"""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    line: int | None
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _line_of(node: ast.AST) -> int | None:
    return getattr(node, "lineno", None)


def _max_nesting_depth(node: ast.AST) -> int:
    """Return maximum nested control-flow depth within a function."""
    control_nodes = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)
    max_depth = 0

    def visit(current: ast.AST, depth: int) -> None:
        nonlocal max_depth
        next_depth = depth + 1 if isinstance(current, control_nodes) else depth
        max_depth = max(max_depth, next_depth)
        for child in ast.iter_child_nodes(current):
            visit(child, next_depth)

    for child in node.body:
        visit(child, 0)
    return max_depth


def analyze_source(source: str, *, long_function_lines: int = 50) -> dict[str, Any]:
    """Analyze Python source and return syntax status, findings, and metrics."""
    findings: list[Finding] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        findings.append(
            Finding(
                rule_id="PY001",
                severity="error",
                line=exc.lineno,
                message=f"Syntax error: {exc.msg}",
            )
        )
        return {
            "syntax_valid": False,
            "findings": [item.to_dict() for item in findings],
            "metrics": {"lines": len(source.splitlines()), "functions": 0, "classes": 0},
        }

    lines = source.splitlines()
    function_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    class_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

            if name in {"eval", "exec"}:
                findings.append(
                    Finding(
                        rule_id="SEC001",
                        severity="high",
                        line=_line_of(node),
                        message=f"Use of {name}() can execute dynamically supplied code; review input trust and alternatives.",
                    )
                )
            elif name == "pickle_loads":
                findings.append(
                    Finding(
                        rule_id="SEC002",
                        severity="high",
                        line=_line_of(node),
                        message="Deserializing untrusted pickle data can execute code; only load trusted data.",
                    )
                )

        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            start = getattr(node, "lineno", 1)
            end = getattr(node, "end_lineno", start)
            length = end - start + 1
            if length > long_function_lines:
                findings.append(
                    Finding(
                        rule_id="QUAL001",
                        severity="medium",
                        line=start,
                        message=f"Function '{node.name}' spans {length} lines; consider smaller focused functions.",
                    )
                )
            depth = _max_nesting_depth(node)
            if depth >= 4:
                findings.append(
                    Finding(
                        rule_id="QUAL002",
                        severity="medium",
                        line=start,
                        message=f"Function '{node.name}' has nested control-flow depth {depth}; consider simplifying.",
                    )
                )

    # Heuristic only: catches common assignment forms, not every possible secret.
    secret_pattern = re.compile(
        r"""(?i)\b(api[_-]?key|secret|password|token)\b\s*=\s*['"][^'"]{8,}['"]"""
    )
    for number, line in enumerate(lines, start=1):
        if secret_pattern.search(line):
            findings.append(
                Finding(
                    rule_id="SEC003",
                    severity="high",
                    line=number,
                    message="Possible hard-coded credential. Move secrets to a secure environment or secret manager.",
                )
            )

    findings.sort(key=lambda item: (item.line or 0, item.rule_id))
    return {
        "syntax_valid": True,
        "findings": [item.to_dict() for item in findings],
        "metrics": {
            "lines": len(lines),
            "functions": len(function_nodes),
            "classes": len(class_nodes),
        },
    }
