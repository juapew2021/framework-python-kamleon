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
        measurement_id,
        user_id=None
    ):

        return requests.get(
            f"{BASE_URL}/api/v1/measurements/{measurement_id}",
            params=(
                {"userId": user_id}
                if user_id is not None
                else None
            )
        )

    def disconnect_measurement(
        self,
        measurement_id
    ):

        return requests.post(
            f"{BASE_URL}/api/v1/measurements/{measurement_id}/disconnect"
        )