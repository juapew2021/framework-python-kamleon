import requests

from config.settings import BASE_URL


class MeasurementClient:

    def create_measurement(
        self,
        payload
    ):

        return requests.post(
            f"{BASE_URL}/api/v1/measurements",
            json=payload
        )

    def get_measurement(
        self,
        measurement_id
    ):

        return requests.get(
            f"{BASE_URL}/api/v1/measurements/{measurement_id}"
        )