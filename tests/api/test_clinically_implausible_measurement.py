import pytest

from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.parametrize(
    ("hydration_score", "ph"),
    [
        # TC-015 (SCRUM-42) + TC-016 (SCRUM-43): hydration score above range
        pytest.param(
            101, 6.2,
            id="score_above_range",
            marks=pytest.mark.xray(["SCRUM-42", "SCRUM-43"])
        ),
        # TC-015 (SCRUM-42) + TC-016 (SCRUM-43): hydration score below range
        pytest.param(
            -1, 6.2,
            id="score_below_range",
            marks=pytest.mark.xray(["SCRUM-42", "SCRUM-43"])
        ),
        # TC-015 (SCRUM-42) + TC-017 (SCRUM-44): pH outside physiological range
        pytest.param(
            75, 14.0,
            id="extreme_ph",
            marks=pytest.mark.xray(["SCRUM-42", "SCRUM-44"])
        )
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
