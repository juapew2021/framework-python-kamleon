import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-35")
@pytest.mark.sanity
def test_insufficient_volume_measurement(
    measurement_service
):

    payload = (
        MeasurementFactory
        .insufficient_volume_measurement()
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

    assert (
        result["result"]
        ["volumeStatus"]
        == "INSUFFICIENT"
    )

    assert (
        result["result"]
        ["hydrationScore"]
        is None
    )