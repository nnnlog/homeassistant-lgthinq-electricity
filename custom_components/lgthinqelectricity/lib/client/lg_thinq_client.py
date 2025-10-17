import logging
import traceback
from datetime import datetime
from typing import Any

import aiohttp
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ...const import DOMAIN
from ..api.auth_api import AuthApi
from ..api.device_api import DeviceApi
from ..model.config import LgThinqConfig
from ..model.exception import UnauthorizedException

_LOGGER = logging.getLogger(__name__)

class LgThinqClient:
    session: aiohttp.ClientSession
    config: LgThinqConfig
    access_token: str = ""

    def __init__(self, session: aiohttp.ClientSession, config: LgThinqConfig):
        self.session = session
        self.config = config

    async def _request(self, callback, retry: bool = True) -> Any:
        """
        All requests except login should be wrapped in this method.
        """
        if self.access_token == "":
            await self.login()

        try:
            return await callback()
        except UnauthorizedException:
            await self.login()
            return await self._request(callback, retry=False)
        except Exception as e:
            if retry:
                _LOGGER.error(f"Error occurred: {e}. Retrying...")
                _LOGGER.error(traceback.format_exc())
                return self._request(callback, retry=False)
            else:
                raise e

    async def login(self) -> None:
        try:
            self.access_token = await AuthApi.get_access_token(self.session, self.config.refresh_token)
        except Exception as e:
            _LOGGER.error(f"Login failed: {e}")
            raise e

    async def _get_available_devices(self) -> list[dict[str, Any]]:
        return await DeviceApi.get_all_devices(self.session, self.access_token, self.config.user_no, self.config.home_id)

    async def get_available_devices(self) -> list[dict[str, Any]]:
        return await self._request(self._get_available_devices)

    async def _get_device_energy_usage_aircon(self, device_id: str) -> int:
        today = datetime.today()
        start_date = today.strftime("%Y-%m-01")
        end_date = today.strftime("%Y-%m-%d")
        target_month = today.strftime("%Y-%m")
        data = await DeviceApi.get_device_energy_history_aircon(self.session, self.access_token, self.config.user_no, device_id, start_date, end_date, "month")
        for datum in data:
            if datum["usedDate"] == target_month:
                return datum["energyData"]
        return 0 # Non-available data returns 0

    async def get_device_energy_usage_aircon(self, device_id: str) -> int:
        return await self._request(lambda: self._get_device_energy_usage_aircon(device_id))

    async def _get_device_energy_usage_laundry(self, device_id: str) -> int:
        today = datetime.today()
        start_date = today.strftime("%Y-%m-01")
        end_date = today.strftime("%Y-%m-%d")
        target_month = today.strftime("%Y-%m")
        data = await DeviceApi.get_device_energy_history_laundry(self.session, self.access_token, self.config.user_no, device_id, start_date, end_date, "month")
        for datum in data:
            if datum["usedDate"] == target_month:
                return datum["periodicEnergyData"]
        return 0 # Non-available data returns 0

    async def get_device_energy_usage_laundry(self, device_id: str) -> int:
        return await self._request(lambda: self._get_device_energy_usage_laundry(device_id))

    async def get_data(self) -> dict[str, Any]:
        devices = await self.get_available_devices()
        data = {}
        for device in devices:
            if device["moduleType"] == "GAM" or device["moduleType"] == "GJM":
                device_id = device["deviceId"]
                energy_data = await self.get_device_energy_usage_aircon(device_id)
                data[device_id] = {
                    "name": "전기 사용량",
                    "info": DeviceInfo(
                        identifiers={(DOMAIN, device["deviceId"])},
                        entry_type=DeviceEntryType.SERVICE,
                        manufacturer="LG Electronics",
                        model=device["modelName"],
                        name=device["alias"],
                    ),
                    "value": float(energy_data) / 1000,  # Convert to kWh
                }
            elif device["moduleType"] == "GWP":
                device_id = device["deviceId"]
                energy_data = await self.get_device_energy_usage_laundry(device_id)
                data[device_id] = {
                    "name": "전기 사용량",
                    "info": DeviceInfo(
                        identifiers={(DOMAIN, device["deviceId"])},
                        entry_type=DeviceEntryType.SERVICE,
                        manufacturer="LG Electronics",
                        model=device["modelName"],
                        name=device["alias"],
                    ),
                    "value": float(energy_data) / 1000,  # Convert to kWh
                }

        return data
