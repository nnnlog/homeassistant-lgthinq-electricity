from __future__ import annotations

import json
import logging
from hashlib import sha256
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import selector, TextSelector, TextSelectorType, TextSelectorConfig

from .lib.api.auth_api import AuthApi
from .lib.api.user_api import UserApi
from .const import DOMAIN, CONF_REFRESH_TOKEN, CONF_ACCESS_TOKEN, CONF_HOME_ID, CONF_USER_NO, CONF_USER_ID

_LOGGER = logging.getLogger(__name__)


class LgThinqConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    _flow_data: dict[str, Any] = None

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        self._flow_data: dict[str, Any] = {}
        return await self.async_step_input_refresh_token(user_input)

    async def async_step_input_refresh_token(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the region selection step."""
        if user_input is not None:
            self._flow_data[CONF_REFRESH_TOKEN] = user_input[CONF_REFRESH_TOKEN]

            websession = async_get_clientsession(self.hass)
            self._flow_data[CONF_ACCESS_TOKEN] = await AuthApi.get_access_token(websession,
                                                                                user_input[CONF_REFRESH_TOKEN])
            user_profile = await UserApi.get_user_profile(websession, self._flow_data[CONF_ACCESS_TOKEN])
            user_id = user_profile["account"]["userID"]
            user_no = user_profile["account"]["userNo"]

            self._flow_data[CONF_USER_ID] = user_id
            self._flow_data[CONF_USER_NO] = user_no

            return await self.async_step_select_home()

        schema = vol.Schema(
            {
                vol.Required(CONF_REFRESH_TOKEN): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.TEXT)
                )
            }
        )

        return self.async_show_form(
            step_id="input_refresh_token", data_schema=schema
        )

    async def async_step_select_home(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the site selection step."""
        if user_input is not None:
            data = json.loads(user_input[CONF_HOME_ID])
            self._flow_data[CONF_HOME_ID] = data["id"]

            unique_id_raw = f"{self._flow_data[CONF_USER_NO]}:{self._flow_data[CONF_HOME_ID]}"
            unique_id = sha256(unique_id_raw.encode("utf-8")).hexdigest()

            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            # Here you would typically validate the credentials and connect to the API
            # If successful, you would store the connection data in self._flow_data
            return self.async_create_entry(
                title=f"LG ThinQ ({self._flow_data[CONF_USER_ID]} - {data["name"]})", data={
                    CONF_REFRESH_TOKEN: self._flow_data[CONF_REFRESH_TOKEN],
                    CONF_USER_NO: self._flow_data[CONF_USER_NO],
                    CONF_HOME_ID: self._flow_data[CONF_HOME_ID],
                })

            return await self.async_step_login()

        websession = async_get_clientsession(self.hass)
        homes = await UserApi.get_all_homes(websession, self._flow_data[CONF_ACCESS_TOKEN],
                                            self._flow_data[CONF_USER_NO])

        data = []
        for home in homes:
            data.append({
                "label": home["homeName"],
                "value": json.dumps({"id": f"{home["homeId"]}", "name": home["homeName"]}),
            })

        schema = vol.Schema(
            {
                vol.Required(CONF_HOME_ID): selector({
                    "select": {
                        "options": data,
                        "sort": True,
                    }
                })
            }
        )

        return self.async_show_form(
            step_id="select_home", data_schema=schema,
        )
