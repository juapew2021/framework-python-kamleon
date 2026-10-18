from factories.measurement_factory import (
    MeasurementFactory
)


def test_backend_unavailable(
    measurement_service
):
    """
    Given the backend is temporarily unavailable
    When a measurement is submitted
    Then submission is retried and the measurement is retained
    Priority: P1
    """

    # Given

    payload = (
        MeasurementFactory
        .backend_unavailable_measurement()
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

    result = (
        measurement_service
        .wait_for_completion(body["measurementId"])
    )
    assert result["status"] == "completed"
    assert result["submissionAttempts"] == 2
