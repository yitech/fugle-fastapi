# Running Unit Tests with Pytest

This project uses `pytest` for running unit tests. Below are examples of how to run tests for specific files, modules, or functions.

## Prerequisites

Ensure that you have `pytest` and `pytest-cov` installed in your virtual environment:

```bash
pip install pytest pytest-cov
```

## Running Tests for the Entire Project

To run all tests across the project and generate a coverage report:

```bash
pytest --cov=app --cov-report=html
```

## Running Tests for a Specific Directory

```bash
pytest tests/crud/ --cov=app --cov-report=html
```

## Running Tests for a Specific Module

```bash
pytest tests/test_crud_order.py --cov=app --cov-report=html
```

## Running Tests for a Specific Test File

```bash
pytest tests/test_main.py --cov=app --cov-report=html
```

## Running Tests for a Specific Test Function

```bash
pytest tests/test_main.py::test_specific_function --cov=app --cov-report=html
```




