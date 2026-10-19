import json
from uuid import uuid4
from pathlib import Path


class MeasurementFactory:

    DATA_FOLDER = (
        Path(__file__).parent.parent
        / "data"
        / "measurements"
    )

    @staticmethod
    def _load(
        filename
    ):

        file_path = (
            MeasurementFactory.DATA_FOLDER
            / filename
        )

        with open(
            file_path,
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def _unique_session(
        payload
    ):

        if "sessionId" in payload:

            payload["sessionId"] = (
                f"SESSION-{uuid4()}"
            )

        return payload

    @staticmethod
    def valid_measurement():

        payload = (
            MeasurementFactory._load(
                "valid_measurement.json"
            )
        )

        return (
            MeasurementFactory
            ._unique_session(
                payload
            )
        )

    @staticmethod
    def anonymous_measurement():

        payload = (
            MeasurementFactory._load(
                "anonymous_measurement.json"
            )
        )

        return (
            MeasurementFactory
            ._unique_session(
                payload
            )
        )

    @staticmethod
    def insufficient_volume_measurement():

        payload = (
            MeasurementFactory._load(
                "insufficient_volume.json"
            )
        )

        return (
            MeasurementFactory
            ._unique_session(
                payload
            )
        )

    @staticmethod
    def duplicate_measurement():

        return (
            MeasurementFactory._load(
                "valid_measurement.json"
            )
        )

    @staticmethod
    def clinically_implausible_measurement(
        hydration_score,
        ph
    ):

        payload = (
            MeasurementFactory._load(
                "valid_measurement.json"
            )
        )

        payload["sensorData"]["ph"] = ph

        payload["sensorData"][
            "hydrationScore"
        ] = hydration_score

        return payload

    @staticmethod
    def buffered_measurements():

        return [
            MeasurementFactory.valid_measurement(),
            MeasurementFactory.valid_measurement(),
            MeasurementFactory.valid_measurement()
        ]

    @staticmethod
    def disconnected_measurement():

        payload = (
            MeasurementFactory.valid_measurement()
        )

        payload["status"] = (
            "disconnected"
        )

        return payload

    @staticmethod
    def malformed_api_response_measurement():

        payload = (
            MeasurementFactory.valid_measurement()
        )

        payload["malformedAnalysis"] = True

        return payload

    @staticmethod
    def firmware_update_request():

        return (
            MeasurementFactory._load(
                "firmware_update_request.json"
            )
        )

    @staticmethod
    def firmware_update_failure_request():

        payload = (
            MeasurementFactory
            .firmware_update_request()
        )

        payload["version"] = (
            "INVALID-VERSION"
        )

        return payload