# ai-code-review-workbench
Python-based automated code evaluation and review system.
# AI Code Review Workbench

A Python-based static code analysis tool that evaluates Python source code, identifies potential security risks, detects code-quality issues, and generates structured JSON reports.

## Overview

AI Code Review Workbench is a lightweight, rule-based code evaluation system designed to help developers identify common issues in Python source files without executing the code being analyzed.

## Features

- **Syntax Validation:** Detects Python syntax errors.
- **Security Analysis:** Flags potentially unsafe use of `eval()` and `exec()`.
- **Credential Detection:** Identifies possible hard-coded API keys, passwords, tokens, and secrets.
- **Code Quality Checks:** Detects unusually long functions and deeply nested control flow.
- **Code Metrics:** Reports lines of code, function count, and class count.
- **JSON Reports:** Generates structured reports for further analysis.
- **Command-Line Interface:** Supports analyzing Python files directly from the terminal.

## Technology Stack

- Python 3.10+
- Python AST (Abstract Syntax Tree)
- Regular Expressions
- JSON
- Unit Testing

## Project Structure

```text
ai-code-review-workbench/
│
├── code_review_workbench/
│   ├── __init__.py
│   ├── analyzer.py
│   └── cli.py
│
├── examples/
│   └── sample.py
│
├── tests/
│   └── test_analyzer.py
│
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/karkiran-del/ai-code-review-workbench.git
```

Navigate to the project directory:

```bash
cd ai-code-review-workbench
```

No external Python packages are currently required.

## Usage

Analyze a Python source file:

```bash
python -m code_review_workbench.cli examples/sample.py
```

Generate a JSON report:

```bash
python -m code_review_workbench.cli examples/sample.py --output report.json
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Design Approach

The analyzer uses Python's built-in AST module to inspect source code structurally. It does not execute the analyzed source file.

The analysis results include syntax validity, detected findings, severity levels, line references, and basic code metrics.

## Current Scope

This project currently implements rule-based static analysis. It does not yet integrate an external AI or large language model.

## Future Improvements

- Expand static analysis rules.
- Add configurable severity levels.
- Improve security vulnerability detection.
- Integrate AI-assisted code review.
- Add automated CI testing.
- Support additional reporting formats.

## Author

**Kiran Shipparkar**

GitHub: [@karkiran-del](https://github.com/karkiran-del)

---

*Built as a Python software engineering project focused on static analysis, code quality, and secure development practices.*
