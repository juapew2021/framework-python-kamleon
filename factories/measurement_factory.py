from uuid import uuid4


class MeasurementFactory:

    @staticmethod
    def valid_measurement():

        return {
            "deviceId": "URINAL-001",
            "userId": "USER-123",
            "sessionId": f"SESSION-{uuid4()}",
            "startedAt": "2026-09-20T10:00:00Z",
            "completedAt": "2026-09-20T10:00:18Z",
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
            "startedAt": "2026-09-20T10:00:00Z",
            "completedAt": "2026-09-20T10:00:18Z",
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
            "startedAt": "2026-09-20T10:00:00Z",
            "completedAt": "2026-09-20T10:00:18Z",
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
            "startedAt": "2026-09-20T10:00:00Z",
            "completedAt": "2026-09-20T10:00:18Z",
            "sensorData": {
                "volume": 320,
                "ph": 14.0,
                "temperature": 36.4
            }
        }

    @staticmethod
    def firmware_update_request():

        return {
            "version": "1.5.0"
        }

    @staticmethod
    def duplicate_measurement():

        return MeasurementFactory.valid_measurement()

    @staticmethod
    def disconnected_measurement():

        return MeasurementFactory.valid_measurement()

    @staticmethod
    def buffered_measurements():

        measurements = []

        for index, started_at in enumerate(
            (
                "2026-09-20T10:00:00Z",
                "2026-09-20T10:01:00Z",
                "2026-09-20T10:02:00Z"
            )
        ):
            measurement = (
                MeasurementFactory
                .valid_measurement()
            )
            measurement["sessionId"] = (
                f"BUFFERED-{uuid4()}"
            )
            measurement["startedAt"] = started_at
            measurement["sensorData"]["volume"] = (
                320 + index
            )
            measurements.append(measurement)

        return [
            measurements[2],
            measurements[0],
            measurements[1]
        ]

    @staticmethod
    def backend_unavailable_measurement():

        measurement = (
            MeasurementFactory
            .valid_measurement()
        )
        measurement["simulateUnavailableAttempts"] = 1

        return measurement

    @staticmethod
    def malformed_api_response_measurement():

        measurement = (
            MeasurementFactory
            .valid_measurement()
        )
        measurement["malformedAnalysis"] = True

        return measurement

    @staticmethod
    def measurement_for_user(user_id):

        measurement = (
            MeasurementFactory
            .valid_measurement()
        )
        measurement["userId"] = user_id

        return measurement

    @staticmethod
    def clinically_implausible_measurement(
        hydration_score=75,
        ph=6.2
    ):

        measurement = (
            MeasurementFactory
            .valid_measurement()
        )
        measurement["sensorData"]["hydrationScore"] = (
            hydration_score
        )
        measurement["sensorData"]["ph"] = ph

        return measurement

    @staticmethod
    def firmware_update_failure_request():

        return {
            "version": "99.0.0",
            "simulateFailure": True
        }