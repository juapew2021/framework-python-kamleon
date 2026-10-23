QA IoT Challenge
Overview

This project implements an automated testing framework for an IoT-based hydration monitoring platform.

The solution focuses on validating the highest-risk business and technical scenarios described in the challenge, including:

Measurement processing
Device management
Firmware updates
Anonymous users
Connectivity failures
Clinical plausibility validation
Data integrity
User access control
Backend resilience

The implementation follows a risk-based testing approach and includes automated regression execution through GitHub Actions.

Framework Architecture

                 GitHub Actions
                         │
                         ▼
                    Pytest Suite
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      API             Integration      Reliability
      Tests             Tests            Tests
                         │
                         ▼
                    Service Layer
                         │
                         ▼
                     API Clients
                         │
                         ▼
                    FastAPI Mock API
                         │
                         ▼
                    Test Data Layer
                      (JSON Files)

Tech Stack

Component	TechnologyLanguage	Python 3.9
Framework	Pytest
Mock API	FastAPI
HTTP Client	Requests
Reporting	Allure
CI/CD	GitHub Actions
Test Data	JSON
Configuration	YAML

Project Structure

framework-python-kamleon/

├── .github/
│   └── workflows/
│       └── regression.yml
│
├── clients/
├── config/
├── data/
│   └── measurements/
│
├── docs/
│   ├── Test_Strategy.md
│   ├── Test_Design.md
│   └── QA_30_60_90_Roadmap.md
│
├── factories/
├── mock_api/
├── reports/
├── services/
├── tests/
│   ├── api/
│   └── integration/
│
├── utils/
│
├── requirements.txt
├── pytest.ini
└── run_qa.sh

Installation

Create a virtual environment:

python3 -m venv venv

Activate:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Running the Mock API

Start the FastAPI mock server:

uvicorn mock_api.app:app --reload

Swagger UI:

http://localhost:8000/docs


Running the Test Suite

Execute the complete regression suite:

pytest -v

Expected result:

17 passed

Generating Allure Report

Generate results:

Shell
pytest -v --alluredir=reports/allure-results

Open report:

Shell
allure serve reports/allure-results

The report includes:

Business domains
Execution steps
Request payloads
Response payloads
Environment information
Severity levels
One-Command Execution

Execute the complete regression suite:

Shell
./run_qa.sh

This command:

Executes all automated tests
Generates Allure results
Generates the report
Opens the report automatically
Implemented Test Coverage
Core Business Flows
ID	ScenarioTC-001	Complete Measurement Lifecycle
TC-002	Device Mode Change
TC-003	Firmware Update
TC-004	Firmware Update Failure
TC-005	Hydration Score Generation
TC-006	Recommendation Generation
Edge Cases
ID	ScenarioTC-007	Anonymous User
TC-008	Insufficient Sample Volume
TC-009	Duplicate Measurement
TC-010	Buffered Measurement Upload
Resilience
ID	ScenarioTC-011	Device Disconnect Mid Measurement
TC-012	Backend Unavailable
TC-013	Invalid API Response
Security & Privacy
ID	ScenarioTC-014	Wrong User Association
Clinical Validation
ID	ScenarioTC-015	Clinically Implausible Result
TC-016	Extreme Hydration Score
TC-017	Extreme pH Value
Technical Decisions
FastAPI Mock

A FastAPI mock service was implemented to simulate the platform APIs and allow deterministic automation execution.

Service Layer

Test logic was separated from API communication through a dedicated service layer.

Benefits:

Better maintainability
Reusable API operations
Clear separation of responsibilities
Factory Pattern

Factories are used to centralize test data generation and avoid duplication.

Data-Driven Testing

Measurement payloads are stored as JSON fixtures.

Benefits:

Easier maintenance
Cleaner test code
Better scalability
Allure Reporting

Allure was selected to provide:

Risk visualization
Business-level grouping
Request and response evidence
Detailed execution tracing
GitHub Actions

CI/CD execution validates the complete regression suite automatically.

Assumptions

The challenge specification leaves some implementation details open to interpretation.

The following assumptions were made:

Hydration scores must remain between 0 and 100.
Duplicate measurements are identified using device and session identifiers.
Firmware updates must fail when an invalid version is requested.
Users cannot access measurements belonging to another user.
Devices can reconnect and upload buffered measurements.
Backend retry logic should prevent immediate test failures during temporary outages.
Contract Ambiguities

Several areas of the challenge do not explicitly define expected behavior.

Examples:

Duplicate detection strategy
Retry limits
Firmware rollback implementation
Clinical plausibility thresholds
User identification priority (QR, RFID, Anonymous)

Reasonable assumptions were implemented to enable automated validation.

CI/CD

The repository contains a GitHub Actions workflow:

Plain Text
.github/workflows/regression.yml

Pipeline responsibilities:

Dependency installation
Mock API startup
Automated regression execution
Allure result generation
Artifact publication
Future Improvements

Given more time, I would implement:

Docker support
Published Allure reports
Contract testing
Performance testing
Security testing
Device simulator framework
Synthetic test data generation
GitHub Pages reporting
API schema validation
Observability validation
AI Usage

Microsoft Copilot and ChatGPT were used as engineering assistants to accelerate framework setup, reporting integration and documentation drafting.

All architectural decisions, debugging activities, implementation validation, risk prioritization, test design decisions and final verification were reviewed and validated manually.

Final Result
Plain Text
✅ 17 Automated Tests
✅ Data-Driven Test Framework
✅ FastAPI Mock API
✅ Allure Reporting
✅ GitHub Actions CI
✅ Risk-Based Test Coverage
✅ Integration and Asynchronous Testing
✅ Security and Resilience Scenarios