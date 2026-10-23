import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-31")
def test_firmware_update_failure(
    device_service
):
    """
    Given a firmware update has started
    When the update fails
    Then the previous firmware remains active
    Priority: P1
    """

    # Given

    device_id = "URINAL-001"
    previous_version = (
        device_service
        .get_device(device_id)
        .json()["firmwareVersion"]
    )

    # When

    response = (
        device_service
        .change_firmware(
            device_id,
            MeasurementFactory
            .firmware_update_failure_request()
        )
    )

    # Then

    assert response.status_code == 502
    assert response.json()["status"] == "update_failed"

    current_device = (
        device_service
        .get_device(device_id)
    )
    assert current_device.status_code == 200
    assert (
        current_device.json()["firmwareVersion"]
        == previous_version
    )
