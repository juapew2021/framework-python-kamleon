import requests

from config.settings import BASE_URL


class DeviceClient:

    def get_device(
        self,
        device_id
    ):

        return requests.get(
            f"{BASE_URL}/api/v1/devices/{device_id}"
        )

    def change_mode(
        self,
        device_id,
        mode
    ):

        return requests.post(
            f"{BASE_URL}/api/v1/devices/{device_id}/mode",
            json={
                "mode": mode
            }
        )