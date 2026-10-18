import time


class InvalidMeasurementResponseError(ValueError):
    pass


class MeasurementProcessingError(RuntimeError):
    pass


class MeasurementSubmissionError(RuntimeError):
    pass


class MeasurementService:

    def __init__(
        self,
        client,
        max_attempts=3
    ):
        self.client = client
        self.max_attempts = max_attempts

    def create_measurement(self, payload):

        for attempt in range(self.max_attempts):
            response = self.client.create_measurement(payload)

            if response.status_code != 503:
                return response

            if attempt == self.max_attempts - 1:
                raise MeasurementSubmissionError(
                    "Measurement submission failed after "
                    f"{self.max_attempts} attempts"
                )

        raise MeasurementSubmissionError(
            "Measurement submission failed"
        )

    def disconnect_measurement(
        self,
        measurement_id
    ):

        return self.client.disconnect_measurement(
            measurement_id
        )

    def get_measurement_for_user(
        self,
        measurement_id,
        user_id
    ):

        return self.client.get_measurement(
            measurement_id,
            user_id=user_id
        )

    def upload_buffered_measurements(
        self,
        measurements
    ):

        ordered_measurements = sorted(
            measurements,
            key=lambda measurement: measurement["startedAt"]
        )

        return [
            self.create_measurement(measurement)
            for measurement in ordered_measurements
        ]

    def wait_for_completion(
        self,
        measurement_id,
        timeout=10
    ):

        start = time.time()

        while time.time() - start < timeout:

            response = (
                self.client
                .get_measurement(
                    measurement_id
                )
            )

            if response.status_code >= 400:
                raise MeasurementProcessingError(
                    "Measurement request failed with "
                    f"HTTP {response.status_code}"
                )

            try:
                body = response.json()
            except ValueError as error:
                raise InvalidMeasurementResponseError(
                    "Measurement API returned invalid JSON"
                ) from error

            if not isinstance(body, dict):
                raise InvalidMeasurementResponseError(
                    "Measurement API response must be an object"
                )

            if body.get("status") not in {
                "processing",
                "completed",
                "failed"
            }:
                raise InvalidMeasurementResponseError(
                    "Measurement API response has an invalid status"
                )

            if body["status"] != "processing":
                if body["status"] == "completed":
                    result = body.get("result")
                    if (
                        not isinstance(result, dict)
                        or "hydrationScore" not in result
                    ):
                        raise InvalidMeasurementResponseError(
                            "Completed measurement response is missing "
                            "hydration analysis"
                        )
                return body

        raise TimeoutError(
            "Measurement never completed"
        )