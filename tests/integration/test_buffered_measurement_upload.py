import pytest
from factories.measurement_factory import (
    MeasurementFactory
)


@pytest.mark.xray("SCRUM-38")
def test_buffered_measurement_upload(
    measurement_service
):
    """
    Given measurements stored locally during offline mode
    When the device reconnects
    Then buffered measurements are uploaded and processed in order
    Priority: P1
    """

    # Given

    buffered_measurements = (
        MeasurementFactory
        .buffered_measurements()
    )
    expected_order = sorted(
        measurement["startedAt"]
        for measurement in buffered_measurements
    )

    # When

    responses = (
        measurement_service
        .upload_buffered_measurements(
            buffered_measurements
        )
    )

    # Then

    assert len(responses) == len(buffered_measurements)
    assert all(response.status_code == 200 for response in responses)

    uploaded_measurements = []
    for response in responses:
        result = (
            measurement_service
            .wait_for_completion(
                response.json()["measurementId"]
            )
        )
        uploaded_measurements.append(result)

    assert [
        measurement["startedAt"]
        for measurement in uploaded_measurements
    ] == expected_order
    assert all(
        measurement["status"] == "completed"
        for measurement in uploaded_measurements
    )
