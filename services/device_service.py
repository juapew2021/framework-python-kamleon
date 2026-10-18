class DeviceService:

    def __init__(
        self,
        client
    ):

        self.client = client

    def get_device(
        self,
        device_id
    ):

        return self.client.get_device(
            device_id
        )

    def change_mode(
        self,
        device_id,
        mode
    ):

        return self.client.change_mode(
            device_id,
            mode
        )

    def change_firmware(
        self,
        device_id,
        payload
    ):

        return self.client.change_firmware(
            device_id,
            payload
        )