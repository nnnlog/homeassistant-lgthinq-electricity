from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_REFRESH_TOKEN, CONF_USER_NO, CONF_HOME_ID, PLATFORMS
from .lib.client.lg_thinq_client import LgThinqClient
from .lib.homeassistant.lg_thinq_data_update_coordinator import LgThinqDataUpdateCoordinator
from .lib.model.config import LgThinqConfigEntryRuntimeData, LgThinqConfig

type LgThinqConfigEntry = ConfigEntry[LgThinqConfigEntryRuntimeData]


async def async_setup_entry(hass: HomeAssistant, entry: LgThinqConfigEntry) -> bool:
    config = LgThinqConfig(
        refresh_token=entry.data[CONF_REFRESH_TOKEN],
        user_no=entry.data[CONF_USER_NO],
        home_id=entry.data[CONF_HOME_ID],
        unique_id=entry.unique_id,
    )

    entry.runtime_data = LgThinqConfigEntryRuntimeData()
    entry.runtime_data.config = config
    entry.runtime_data.coordinator = LgThinqDataUpdateCoordinator(hass,
                                                                  LgThinqClient(async_get_clientsession(hass), config))

    await entry.runtime_data.coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: LgThinqConfigEntry) -> bool:
    await entry.runtime_data.coordinator.async_shutdown()

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
