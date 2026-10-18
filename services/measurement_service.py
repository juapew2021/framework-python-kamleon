import time


class MeasurementService:

    def __init__(self, client):
        self.client = client

    def create_measurement(self, payload):

        return self.client.create_measurement(
            payload
        )

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

            body = response.json()

            if body["status"] != "processing":
                return body

        raise TimeoutError(
            "Measurement never completed"
        )