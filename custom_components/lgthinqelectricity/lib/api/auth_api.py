import time
from typing import Any

import aiohttp

from .const import MODEL_NAME, OS_VERSION, USER_AGENT_GENERAL, APP_KEY, APP_VERSION_WITH_APP
from .signature import Signature
from ..model.exception import UnauthorizedException


class AuthApi:
    @staticmethod
    async def get_current_time_from_server(websession: aiohttp.ClientSession) -> dict[str, Any]:
        async with websession.get("https://kr.lgeapi.com/datetime", headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": USER_AGENT_GENERAL,
            "Accept": "application/json",
        }) as response:
            response.raise_for_status()
            return await response.json()

    @staticmethod
    async def get_current_timestamp() -> str:
        return str(int(time.time()))

    @staticmethod
    async def get_access_token(websession: aiohttp.ClientSession, refresh_token: str) -> str:
        current_time = await AuthApi.get_current_time_from_server(websession)
        date = current_time["date"]

        body = f"grant_type=refresh_token&refresh_token={refresh_token}"
        path = "/oauth/1.0/oauth2/token"
        signature = Signature.calculate_signature(f"{path}?{body}\n{date}")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "X-Lge-Oauth-Signature": signature,
            "X-Lge-Oauth-Date": date,
            "Accept": "application/json",
            "X-Lge-Appkey": APP_KEY,
            "X-Lge-App-Os": "ANDROID",
            "X-Model-Name": MODEL_NAME,
            "X-Os-Version": OS_VERSION,
            "X-App-Version": APP_VERSION_WITH_APP,
            "User-Agent": USER_AGENT_GENERAL,
        }

        async with websession.post("https://kr.lgeapi.com/oauth/1.0/oauth2/token", headers=headers, data=body) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return (await response.json())["access_token"]