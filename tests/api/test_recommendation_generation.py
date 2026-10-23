import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-33")
@pytest.mark.smoke
def test_recommendation_generated(
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

    recommendation = (
        result["result"]
        ["recommendation"]
    )

    assert recommendation is not None
    assert len(recommendation) > 0