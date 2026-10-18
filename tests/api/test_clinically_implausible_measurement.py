import pytest

from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.parametrize(
    ("hydration_score", "ph"),
    [
        (101, 6.2),
        (-1, 6.2),
        (75, 14.0)
    ]
)
def test_clinically_implausible_measurement(
    measurement_service,
    hydration_score,
    ph
):
    """
    Given technically valid sensor data
    When the hydration analysis is clinically implausible
    Then the result is flagged as suspicious
    Priority: P1
    """

    # Given

    response = (
        measurement_service
        .create_measurement(
            MeasurementFactory
            .clinically_implausible_measurement(
                hydration_score=hydration_score,
                ph=ph
            )
        )
    )
    measurement_id = (
        response.json()["measurementId"]
    )

    # When

    result = (
        measurement_service
        .wait_for_completion(measurement_id)
    )

    # Then

    assert result["status"] == "completed"
    assert (
        result["result"]["clinicalStatus"]
        == "SUSPICIOUS"
    )
