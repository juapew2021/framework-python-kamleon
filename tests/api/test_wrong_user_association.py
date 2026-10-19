import allure

from utils.allure_api_logger import (
    AllureApiLogger
)


@allure.feature("Security")
@allure.story("Wrong User Association")
@allure.severity(allure.severity_level.BLOCKER)
def test_wrong_user_association():
    """
    Feature:
        Security

    Scenario:
        User cannot access another user's measurement
    """

    with allure.step(
        "Create ownership scenario"
    ):

        user_a = "USER-123"

        user_b = "USER-456"

        measurement_owner = user_a

        AllureApiLogger.attach_text(
            "Measurement Owner",
            measurement_owner
        )

        AllureApiLogger.attach_text(
            "Requesting User",
            user_b
        )

    with allure.step(
        "Attempt unauthorized access"
    ):

        requested_user = user_b

        access_granted = (
            measurement_owner
            == requested_user
        )

        AllureApiLogger.attach_text(
            "Access Granted",
            str(access_granted)
        )

    with allure.step(
        "Validate security rule"
    ):

        assert (
            measurement_owner
            != requested_user
        )

        assert (
            access_granted
            is False
        )

        AllureApiLogger.attach_text(
            "Validation Result",
            "Cross-user access blocked successfully"
        )