import pytest
import allure

from factories.measurement_factory import (
    MeasurementFactory
)

from utils.allure_api_logger import (
    AllureApiLogger
)


@allure.feature("Measurement Processing")
@allure.story("Complete Measurement Lifecycle")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.xray("SCRUM-28")
def test_measurement_complete_flow(
    measurement_service
):
    """
    Feature:
        Measurement Processing

    Scenario:
        Complete measurement lifecycle
    """

    with allure.step(
        "Create measurement request"
    ):

        payload = (
            MeasurementFactory
            .valid_measurement()
        )

        response = (
            measurement_service
            .create_measurement(
                payload
            )
        )

        AllureApiLogger.attach_request(
            endpoint="/api/v1/measurements",
            method="POST",
            payload=payload
        )

        AllureApiLogger.attach_response(
            response
        )

        assert response.status_code == 200

    with allure.step(
        "Validate measurement created"
    ):

        body = response.json()

        assert (
            body["status"]
            == "processing"
        )

        measurement_id = (
            body["measurementId"]
        )

        AllureApiLogger.attach_text(
            "Measurement ID",
            measurement_id
        )

    with allure.step(
        "Wait for measurement completion"
    ):

        result = (
            measurement_service
            .wait_for_completion(
                measurement_id
            )
        )

        AllureApiLogger.attach_json(
            "Completed Measurement Response",
            result
        )

    with allure.step(
        "Validate hydration result"
    ):

        assert (
            result["status"]
            == "completed"
        )

        assert (
            result["result"]
            is not None
        )

        assert (
            result["result"]["hydrationScore"]
            >= 0
        )

        assert (
            result["result"]["hydrationScore"]
            <= 100
        )

        assert (
            result["result"]["hydrationStatus"]
            == "VERY_WELL_HYDRATED"
        )

        assert (
            result["result"]["recommendation"]
            is not None
        )