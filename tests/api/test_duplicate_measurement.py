import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-36")
@pytest.mark.sanity
def test_duplicate_measurement(
    measurement_service
):
    """
    Given an existing measurement
    When the same measurement is submitted twice
    Then the system detects the duplicate without processing it twice
    Priority: P1
    """

    # Given

    payload = (
        MeasurementFactory
        .duplicate_measurement()
    )
    first_response = (
        measurement_service
        .create_measurement(payload)
    )
    measurement_id = (
        first_response.json()["measurementId"]
    )

    # When

    duplicate_response = (
        measurement_service
        .create_measurement(payload)
    )

    # Then

    assert duplicate_response.status_code == 200
    duplicate = duplicate_response.json()
    assert duplicate["status"] == "duplicate"
    assert duplicate["duplicate"] is True
    assert duplicate["measurementId"] == measurement_id

    stored_measurement = (
        measurement_service
        .client
        .get_measurement(measurement_id)
        .json()
    )
    assert stored_measurement["processingCount"] == 1
