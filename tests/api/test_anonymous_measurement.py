from factories.measurement_factory import (
    MeasurementFactory
)


def test_anonymous_measurement(
    measurement_service
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

    assert response.status_code == 200

    measurement_id = (
        response.json()["measurementId"]
    )

    result = (
        measurement_service
        .wait_for_completion(
            measurement_id
        )
    )

    assert result["status"] == "completed"

    assert result["userId"] is None

    assert result["result"] is not None