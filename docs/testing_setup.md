# Testing Setup Guide

## Table of Contents

- [Testing Setup Guide](#testing-setup-guide)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Writing Tests](#writing-tests)
  - [Running Tests](#running-tests)
  - [Test Coverage](#test-coverage)


## Prerequisites

- Python 3.6+ installed
- `pytest` package installed (will be installed via requirements)

## Setup

1. Install test dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `tests` directory in your project root:

```
scripts/
├── ...
└── tests/
    ├── __init__.py
    ├── test_directory_tree.py
    └── test_treemd.py
```

## Writing Tests

1. Create test files following the naming pattern `test_*.py`
2. Write test functions prefixed with `test_`

Example test (`test_directory_tree.py`):

```python
from core.directory_tree import DirectoryTree

def test_empty_tree():
    tree = DirectoryTree()
    assert tree.root is None
```

## Running Tests

Run all tests:

```bash
pytest
```

Run specific test file:

```bash
pytest tests/test_directory_tree.py
```

Run with verbose output:

```bash
pytest -v
```

## Test Coverage

To check test coverage:

```bash
pip install pytest-cov
pytest --cov=core --cov=scripts
```

This will show which parts of your code are covered by tests.
