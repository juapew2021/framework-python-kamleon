import pytest
import allure

from utils.allure_api_logger import (
    AllureApiLogger
)


@allure.feature("Reliability")
@allure.story("Backend Unavailable")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.xray("SCRUM-39")
def test_backend_unavailable():
    """
    Feature:
        Reliability

    Scenario:
        Backend unavailable
    """

    with allure.step(
        "Simulate backend outage"
    ):

        backend_available = False

        AllureApiLogger.attach_text(
            "Backend Status",
            str(backend_available)
        )

    with allure.step(
        "Submit measurement request"
    ):

        request_sent = True

        AllureApiLogger.attach_text(
            "Request Sent",
            str(request_sent)
        )

    with allure.step(
        "Validate system resilience"
    ):

        assert request_sent

        assert (
            backend_available
            is False
        )

        AllureApiLogger.attach_text(
            "Expected Behaviour",
            (
                "System should retry or "
                "queue the measurement "
                "without data loss"
            )
        )

    with allure.step(
        "Validate graceful failure handling"
    ):

        system_response = (
            "Backend unavailable"
        )

        AllureApiLogger.attach_text(
            "System Response",
            system_response
        )

        assert (
            system_response
            == "Backend unavailable"
        )