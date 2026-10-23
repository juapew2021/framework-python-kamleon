import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-37")
def test_device_disconnect_mid_measurement(
    measurement_service
):
    """
    Given a measurement in progress
    When the device disconnects
    Then measurement processing stops safely
    Priority: P1
    """

    # Given

    response = (
        measurement_service
        .create_measurement(
            MeasurementFactory
            .disconnected_measurement()
        )
    )
    measurement_id = (
        response.json()["measurementId"]
    )

    # When

    disconnect_response = (
        measurement_service
        .disconnect_measurement(measurement_id)
    )

    # Then

    assert disconnect_response.status_code == 200
    assert disconnect_response.json()["status"] == "failed"

    result = (
        measurement_service
        .wait_for_completion(measurement_id)
    )
    assert result["status"] == "failed"
    assert (
        result["failureReason"]
        == "Device disconnected during measurement"
    )
