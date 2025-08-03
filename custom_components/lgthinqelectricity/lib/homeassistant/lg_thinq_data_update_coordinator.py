from logging import Logger
from typing import Any
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..client.lg_thinq_client import LgThinqClient


class LgThinqDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    logger: Logger = Logger("lgthinq_data_update_coordinator")
    config_entry: ConfigEntry

    client: LgThinqClient

    def __init__(self, hass: HomeAssistant, client: LgThinqClient) -> None:
        super().__init__(
            hass,
            logger=self.logger,
            name="lgthinq_data_update_coordinator",
            update_interval=timedelta(seconds=10),
            update_method=self._async_update_data,
        )

        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        return await self.client.get_data()
