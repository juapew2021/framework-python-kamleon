class MeasurementFactory:

    @staticmethod
    def valid_measurement():

        return {
            "deviceId": "URINAL-001",

            "userId": "USER-123",

            "sessionId": "SESSION-456",

            "startedAt":
                "2026-09-20T10:00:00Z",

            "completedAt":
                "2026-09-20T10:00:18Z",

            "sensorData": {
                "volume": 320,
                "ph": 6.2,
                "temperature": 36.4
            }
        }

    @staticmethod
    def insufficient_volume_measurement():

        return {
            "deviceId": "URINAL-001",

            "userId": "USER-123",

            "sessionId": "SESSION-999",

            "startedAt":
                "2026-09-20T10:00:00Z",

            "completedAt":
                "2026-09-20T10:00:18Z",

            "sensorData": {
                "volume": 50,
                "ph": 6.2,
                "temperature": 36.4
            }
        }

    @staticmethod
    def anonymous_measurement():

        return {
            "deviceId": "URINAL-001",

            "userId": None,

            "sessionId": "SESSION-777",

            "startedAt":
                "2026-09-20T10:00:00Z",

            "completedAt":
                "2026-09-20T10:00:18Z",

            "sensorData": {
                "volume": 320,
                "ph": 6.2,
                "temperature": 36.4
            }
        }

    @staticmethod
    def extreme_ph_measurement():

        return {
            "deviceId": "URINAL-001",

            "userId": "USER-123",

            "sessionId": "SESSION-888",

            "startedAt":
                "2026-09-20T10:00:00Z",

            "completedAt":
                "2026-09-20T10:00:18Z",

            "sensorData": {
                "volume": 320,
                "ph": 14.0,
                "temperature": 36.4
            }
        }