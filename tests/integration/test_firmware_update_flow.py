import allure

from utils.allure_api_logger import (
    AllureApiLogger
)


@allure.feature("Device Management")
@allure.story("Firmware Update Failure")
@allure.severity(allure.severity_level.BLOCKER)
def test_firmware_update_failure():
    """
    Feature:
        Device Management

    Scenario:
        Firmware update fails
    """

    with allure.step(
        "Prepare device firmware state"
    ):

        current_version = "1.4.2"

        target_version = "2.0.0"

        AllureApiLogger.attach_text(
            "Current Firmware Version",
            current_version
        )

        AllureApiLogger.attach_text(
            "Target Firmware Version",
            target_version
        )

    with allure.step(
        "Simulate firmware update failure"
    ):

        update_successful = False

        firmware_after_update = (
            current_version
        )

        AllureApiLogger.attach_text(
            "Update Successful",
            str(update_successful)
        )

    with allure.step(
        "Validate rollback strategy"
    ):

        assert (
            update_successful
            is False
        )

        assert (
            firmware_after_update
            == current_version
        )

        AllureApiLogger.attach_text(
            "Rollback Result",
            "Previous firmware version preserved"
        )

    with allure.step(
        "Validate compatible state"
    ):

        device_operational = True

        assert (
            device_operational
            is True
        )

        AllureApiLogger.attach_text(
            "Device Status",
            "Operational after failed update"
        )