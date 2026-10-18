import pytest

from factories.measurement_factory import (
    MeasurementFactory
)
from services.measurement_service import (
    InvalidMeasurementResponseError
)


def test_invalid_api_response(
    measurement_service
):
    """
    Given the Data API returns a malformed payload
    When hydration processing occurs
    Then the payload is rejected with a controlled error
    Priority: P2
    """

    # Given

    response = (
        measurement_service
        .create_measurement(
            MeasurementFactory
            .malformed_api_response_measurement()
        )
    )
    measurement_id = (
        response.json()["measurementId"]
    )

    # When / Then

    with pytest.raises(
        InvalidMeasurementResponseError,
        match="missing hydration analysis"
    ):
        measurement_service.wait_for_completion(
            measurement_id
        )
