import allure
import pytest

from factories.measurement_factory import (
    MeasurementFactory
)


@allure.feature("Device Management")
@allure.story("Firmware Update Success")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.xray("SCRUM-30")
@pytest.mark.smoke
def test_firmware_update_success(
    device_service
):
    """
    Given a registered device with a known firmware version
    When a firmware update to a valid version is requested
    Then the update is accepted
    And the device reports the new firmware version
    Priority: P1
    """

    device_id = "URINAL-001"
    request = MeasurementFactory.firmware_update_request()
    target_version = request["version"]

    with allure.step("Get current firmware version"):

        device = device_service.get_device(device_id)

        assert device.status_code == 200

    with allure.step("Request firmware update to a valid version"):

        response = device_service.change_firmware(
            device_id,
            request
        )

        assert response.status_code == 200

        body = response.json()

        assert body["deviceId"] == device_id
        assert body["status"] == "update_started"
        assert body["targetVersion"] == target_version

    with allure.step("Validate device reports the new firmware"):

        current_device = device_service.get_device(device_id)

        assert current_device.status_code == 200
        assert (
            current_device.json()["firmwareVersion"]
            == target_version
        )
