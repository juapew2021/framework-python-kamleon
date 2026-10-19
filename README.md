QA IoT Challenge
Automated testing framework for an IoT hydration monitoring platform.

Overview
This solution focuses on validating the most critical business and technical risks across the platform.

The framework uses:

Python
Pytest
FastAPI
Requests
YAML-based configuration
The architecture follows a layered approach:

Tests
 ↓
Services
 ↓
Clients
 ↓
Mock API

Project Structure **

qa-iot-challenge/

├── assertions/
├── clients/
├── config/
├── factories/
├── mock_api/
├── services/
├── tests/
│   ├── api/
│   ├── integration/
│   └── features/
├── requirements.txt
└── pytest.ini

Installation

Create virtual environment:

Activate:

Shell
source venv/bin/activate

Install dependencies:

Shell
pip install -r requirements.txt

Running Mock API
Shell
uvicorn mock_api.app:app --reload

Swagger:

Plain Text
http://localhost:8000/docs

Running Tests

Run all tests:

Shell
pytest -v

Run a specific test:

Shell
pytest tests/api/test_anonymous_measurement.py -v

Implemented Test Scenarios
Positive Scenarios
Measurement Processing Flow
Device Mode Change
Firmware Update
Hydration Score Generation
Recommendation Generation
Negative and Edge Cases
Anonymous User
Insufficient Volume
Duplicate Measurements
Invalid API Response
Backend Unavailable
Wrong User Association
Clinically Implausible Results
Device Disconnect Mid Measurement
Buffered Measurements Upload
Firmware Update Failure
Risk-Based Strategy

Prioritisation was based on business impact and technical risk.

Highest priority areas:

Measurement Processing
Data Integrity
User Association
Clinical Plausibility
Device Connectivity
Firmware Management
Assumptions
Mock API simulates asynchronous processing.
Hydration results are generated after measurement completion.
Sample volume below threshold invalidates analysis.
Anonymous users are supported.
Devices may reconnect with buffered measurements.

---

# Siguiente entregable: Test Strategy (Parte 1)

Si seguimos una estrategia profesional, la resumiría así:

### Objetivo

Garantizar que:

```text
Measurements are processed correctly
Users receive valid hydration results
Data integrity is preserved
Device failures are handled safely

Pirámide de pruebas
Plain Text
E2E
▲
Integration Tests
▲
API Tests
Riesgos priorizados
Wrong User Association
Data Loss
Invalid Measurements
Device Offline / Reconnect
Firmware Failures
Clinical Plausibility
Backend Availability
Automatización
Plain Text
Pytest
Mock API
Risk-based coverage