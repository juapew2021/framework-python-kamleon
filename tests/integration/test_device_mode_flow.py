import pytest

@pytest.mark.xray("SCRUM-29")
def test_change_device_to_maintenance_mode(
    device_service
):
    """
    Feature:
        Device Management

    Scenario:
        Change device mode

    Given
        an existing device

    When
        maintenance mode is requested

    Then
        device mode should be maintenance
    """

    # Given

    device_id = "URINAL-001"

    # When

    response = (
        device_service
        .change_mode(
            device_id,
            "maintenance"
        )
    )

    # Then

    assert response.status_code == 200

    body = response.json()

    assert (
        body["deviceId"]
        == device_id
    )

    assert (
        body["mode"]
        == "maintenance"
    )

    # When

    current_device = (
        device_service
        .get_device(
            device_id
        )
    )

    # Then

    assert (
        current_device.status_code
        == 200
    )

    assert (
        current_device.json()["mode"]
        == "maintenance"
    )