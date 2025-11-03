## FastAPI Calculator — Tests, Logging & CI/CD

### Overview

This project is a FastAPI-based calculator that performs basic arithmetic operations such as addition, subtraction, multiplication, division, and power.
It includes:

✅ Unit, integration, and end-to-end (E2E) tests

✅ Structured logging for requests, operations, and errors

✅ Continuous Integration (CI) setup via GitHub Actions

✅ A minimal browser UI for interactive calculations


### Logging
Logs are configured in app/logger_setup.py and enabled globally.
Each request and operation is logged with timestamp, level, and details.

Example log output:
2025-11-01 13:45:10 | INFO | calculator.app | REQ POST /api/calc
2025-11-01 13:45:10 | INFO | calculator.app | Calculate: 10 add 7
2025-11-01 13:45:10 | INFO | calculator.app | Result: 17


### Continuous Integration (CI)

This project uses GitHub Actions to automatically:

Install dependencies

Install Playwright browsers

Run all tests (unit, integration, and E2E)

Workflow: .github/workflows/ci.yml

### Key Features

Clean separation of concerns (operations, schemas, logging, app)

Complete automated test coverage

Browser-based E2E tests using Playwright

Ready-to-use CI pipeline

Lightweight UI with live calculation

python -m uvicorn app.main:app --reload (for running the website)