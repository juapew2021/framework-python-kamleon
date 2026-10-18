from fastapi import FastAPI
from uuid import uuid4

app = FastAPI()

# ==================================================
# In-memory storage
# ==================================================

measurements = {}

devices = {
    "URINAL-001": {
        "deviceId": "URINAL-001",
        "status": "online",
        "mode": "normal",
        "firmwareVersion": "1.4.2",
        "lastSeen": "2026-09-20T11:02:10Z"
    }
}


# ==================================================
# Health Check
# ==================================================

@app.get("/")
def health():
    return {
        "status": "running"
    }


# ==================================================
# Measurements
# ==================================================

@app.post("/api/v1/measurements")
def create_measurement(payload: dict):

    measurement_id = f"MEAS-{uuid4()}"

    measurements[measurement_id] = {
        "measurementId": measurement_id,
        "deviceId": payload["deviceId"],
        "userId": payload.get("userId"),
        "sensorData": payload.get("sensorData", {}),
        "status": "processing",
        "result": None,
        "poll_count": 0
    }

    return {
        "measurementId": measurement_id,
        "status": "processing"
    }


@app.get("/api/v1/measurements/{measurement_id}")
def get_measurement(measurement_id: str):

    if measurement_id not in measurements:
        return {
            "error": "Measurement not found"
        }

    measurement = measurements[measurement_id]

    measurement["poll_count"] += 1

    if (
        measurement["status"] == "processing"
        and measurement["poll_count"] >= 3
    ):

        volume = (
            measurement["sensorData"]
            .get("volume", 320)
        )

        measurement["status"] = "completed"

        # ==================================================
        # Business Rule:
        # Insufficient volume
        # ==================================================

        if volume < 100:

            measurement["result"] = {
                "hydrationScore": None,
                "hydrationStatus": None,

                "electrolytes": None,
                "electrolyteStatus": None,

                "volume": volume,
                "volumeStatus": "INSUFFICIENT",

                "recommendation":
                    "Sample volume too low for a valid analysis."
            }

        else:

            measurement["result"] = {
                "hydrationScore": 75,
                "hydrationStatus":
                    "VERY_WELL_HYDRATED",

                "electrolytes": 25,
                "electrolyteStatus":
                    "BALANCED",

                "volume": volume,
                "volumeStatus":
                    "EXCELLENT",

                "recommendation":
                    "Consider drinking electrolyte beverages."
            }

    return measurement


# ==================================================
# Devices
# ==================================================

@app.get("/api/v1/devices/{device_id}")
def get_device(device_id: str):

    if device_id not in devices:

        return {
            "error": "Device not found"
        }

    return devices[device_id]


@app.post("/api/v1/devices/{device_id}/mode")
def change_device_mode(
    device_id: str,
    payload: dict
):

    if device_id not in devices:

        return {
            "error": "Device not found"
        }

    devices[device_id]["mode"] = payload["mode"]

    return {
        "deviceId": device_id,
        "mode": payload["mode"]
    }


@app.post(
    "/api/v1/devices/{device_id}/firmware-update"
)
def firmware_update(
    device_id: str,
    payload: dict
):

    if device_id not in devices:

        return {
            "error": "Device not found"
        }

    target_version = payload["version"]

    devices[device_id][
        "firmwareVersion"
    ] = target_version

    return {
        "deviceId": device_id,
        "status": "update_started",
        "targetVersion": target_version
    }