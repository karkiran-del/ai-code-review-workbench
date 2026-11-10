"""Command-line interface for the workbench."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_source


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run safe, rule-based static checks on a Python source file."
    )
    parser.add_argument("file", type=Path, help="Path to a Python source file")
    parser.add_argument("--output", type=Path, help="Optional path for a JSON report")
    args = parser.parse_args()

    try:
        source = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(f"Cannot read {args.file}: {exc}")

    report = analyze_source(source)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(rendered)

    return 0 if report["syntax_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
