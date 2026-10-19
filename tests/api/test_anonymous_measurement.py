import allure

from factories.measurement_factory import (
    MeasurementFactory
)

from utils.allure_api_logger import (
    AllureApiLogger
)


@allure.feature("Measurement Processing")
@allure.story("Anonymous User")
@allure.severity(allure.severity_level.CRITICAL)
def test_anonymous_measurement(
    measurement_service
):
    """
    Feature:
        Anonymous Measurement

    Scenario:
        Anonymous user submits sample
    """

    with allure.step(
        "Create anonymous measurement"
    ):

        payload = (
            MeasurementFactory
            .anonymous_measurement()
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

        assert (
            response.status_code
            == 200
        )

    with allure.step(
        "Validate measurement creation"
    ):

        measurement_id = (
            response.json()[
                "measurementId"
            ]
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
        "Validate anonymous user processing"
    ):

        assert (
            result["status"]
            == "completed"
        )

        assert (
            result["userId"]
            is None
        )

        assert (
            result["result"]
            is not None
        )

        AllureApiLogger.attach_text(
            "Validation Result",
            "Anonymous measurement successfully processed"
        )
