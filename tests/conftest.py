import pytest

from clients.measurement_client import (
    MeasurementClient
)

from services.measurement_service import (
    MeasurementService
)

from clients.device_client import (
    DeviceClient
)

from services.device_service import (
    DeviceService
)


# =========================
# Measurement Fixtures
# =========================

@pytest.fixture
def measurement_client():

    return MeasurementClient()


@pytest.fixture
def measurement_service(
    measurement_client
):

    return MeasurementService(
        measurement_client
    )


# =========================
# Device Fixtures
# =========================

@pytest.fixture
def device_client():

    return DeviceClient()


@pytest.fixture
def device_service(
    device_client
):

    return DeviceService(
        device_client
    )