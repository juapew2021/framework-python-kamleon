from factories.measurement_factory import (
    MeasurementFactory
)


def test_firmware_update_flow(
    device_client
):
    """
    Feature:
        Device Firmware Management

    Scenario:
        Update device firmware
    """

    # Given

    device_id = "URINAL-001"

    payload = (
        MeasurementFactory
        .firmware_update_request()
    )

    # When

    response = (
        device_client
        .change_firmware(
            device_id,
            payload
        )
    )

    # Then

    assert (
        response.status_code
        == 200
    )

    body = response.json()

    assert (
        body["status"]
        == "update_started"
    )

    assert (
        body["targetVersion"]
        == "1.5.0"
    )