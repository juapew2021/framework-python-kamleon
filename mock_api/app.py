from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uuid import uuid4

app = FastAPI()

# ==================================================
# In-memory storage
# ==================================================

measurements = {}
measurement_sessions = {}
submission_attempts = {}

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

    session_key = (
        payload.get("deviceId"),
        payload.get("sessionId")
    )

    if session_key in measurement_sessions:
        existing_id = measurement_sessions[session_key]
        return {
            "measurementId": existing_id,
            "status": "duplicate",
            "duplicate": True
        }

    attempt_count = (
        submission_attempts.get(session_key, 0) + 1
    )
    submission_attempts[session_key] = attempt_count

    unavailable_attempts = payload.get(
        "simulateUnavailableAttempts",
        0
    )
    if attempt_count <= unavailable_attempts:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Measurement backend unavailable",
                "attempt": attempt_count
            }
        )

    measurement_id = f"MEAS-{uuid4()}"

    measurements[measurement_id] = {
        "measurementId": measurement_id,
        "deviceId": payload["deviceId"],
        "userId": payload.get("userId"),
        "sessionId": payload.get("sessionId"),
        "startedAt": payload.get("startedAt"),
        "completedAt": payload.get("completedAt"),
        "sensorData": payload.get("sensorData", {}),
        "status": "processing",
        "result": None,
        "poll_count": 0,
        "processingCount": 1,
        "submissionAttempts": attempt_count,
        "malformedAnalysis": payload.get(
            "malformedAnalysis",
            False
        )
    }
    measurement_sessions[session_key] = measurement_id

    return {
        "measurementId": measurement_id,
        "status": "processing"
    }


@app.get("/api/v1/measurements/{measurement_id}")
def get_measurement(
    measurement_id: str,
    userId: str = None
):

    if measurement_id not in measurements:
        return JSONResponse(
            status_code=404,
            content={"error": "Measurement not found"}
        )

    measurement = measurements[measurement_id]

    if (
        userId is not None
        and measurement["userId"] != userId
    ):
        return JSONResponse(
            status_code=403,
            content={"error": "Access denied"}
        )

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

            hydration_score = (
                measurement["sensorData"]
                .get("hydrationScore", 75)
            )
            ph = (
                measurement["sensorData"]
                .get("ph", 6.2)
            )
            suspicious = (
                hydration_score < 0
                or hydration_score > 100
                or ph < 4.0
                or ph > 9.0
            )

            measurement["result"] = {
                "hydrationScore": hydration_score,
                "hydrationStatus":
                    "VERY_WELL_HYDRATED",

                "electrolytes": 25,
                "electrolyteStatus":
                    "BALANCED",

                "volume": volume,
                "volumeStatus":
                    "EXCELLENT",

                "recommendation":
                    "Consider drinking electrolyte beverages.",
                "clinicalStatus": (
                    "SUSPICIOUS"
                    if suspicious
                    else "PLAUSIBLE"
                )
            }

        if measurement["malformedAnalysis"]:
            measurement["result"] = {
                "hydrationStatus": "VERY_WELL_HYDRATED"
            }

    return measurement


@app.post(
    "/api/v1/measurements/{measurement_id}/disconnect"
)
def disconnect_measurement(measurement_id: str):

    if measurement_id not in measurements:
        return JSONResponse(
            status_code=404,
            content={"error": "Measurement not found"}
        )

    measurement = measurements[measurement_id]
    if measurement["status"] == "processing":
        measurement["status"] = "failed"
        measurement["failureReason"] = (
            "Device disconnected during measurement"
        )

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

    if target_version == "INVALID-VERSION":

        return JSONResponse(
            status_code=502,
            content={
                "deviceId": device_id,
                "status": "update_failed",
                "targetVersion": target_version,
                "error": "Firmware update failed"
            }
        )

    devices[device_id][
        "firmwareVersion"
    ] = target_version

    return {
        "deviceId": device_id,
        "status": "update_started",
        "targetVersion": target_version
    }