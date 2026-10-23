import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-32")
@pytest.mark.smoke
def test_hydration_score_generation(
    measurement_service
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

    measurement_id = (
        response.json()[
            "measurementId"
        ]
    )

    result = (
        measurement_service
        .wait_for_completion(
            measurement_id
        )
    )

    hydration_score = (
        result["result"]
        ["hydrationScore"]
    )

    assert hydration_score >= 0
    assert hydration_score <= 100