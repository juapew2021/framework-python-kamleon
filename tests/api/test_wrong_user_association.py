from factories.measurement_factory import (
    MeasurementFactory
)


def test_wrong_user_association(
    measurement_service
):
    """
    Given a measurement belongs to User A
    When User B requests the measurement
    Then access is denied
    Priority: P1
    """

    # Given

    response = (
        measurement_service
        .create_measurement(
            MeasurementFactory
            .measurement_for_user("USER-A")
        )
    )
    measurement_id = (
        response.json()["measurementId"]
    )

    # When

    unauthorized_response = (
        measurement_service
        .get_measurement_for_user(
            measurement_id,
            "USER-B"
        )
    )

    # Then

    assert unauthorized_response.status_code == 403
    assert unauthorized_response.json()["error"] == "Access denied"
