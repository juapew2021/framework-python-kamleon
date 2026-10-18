from factories.measurement_factory import (
    MeasurementFactory
)


def test_measurement_complete_flow(
    measurement_service
):
    """
    Feature:
        Measurement Processing

    Scenario:
        Complete measurement lifecycle
    """

    # Given
    payload = (
        MeasurementFactory
        .valid_measurement()
    )

    # When
    response = (
        measurement_service
        .create_measurement(payload)
    )

    # Then
    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "processing"

    measurement_id = body["measurementId"]

    # When
    result = (
        measurement_service
        .wait_for_completion(
            measurement_id
        )
    )

    # Then
    assert result["status"] == "completed"
    assert result["result"] is not None
    assert result["result"]["hydration"] == 72