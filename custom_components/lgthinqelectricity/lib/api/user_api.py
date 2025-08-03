from typing import Any

import aiohttp

from .auth_api import AuthApi
from .const import APP_KEY, USER_AGENT_GENERAL, APP_VERSION_WITH_APP, MODEL_NAME, OS_VERSION, \
    CLIENT_ID, \
    USER_AGENT_OKHTTP, APP_VERSION, API_KEY
from .signature import Signature
from ..model.exception import UnauthorizedException


class UserApi:
    @staticmethod
    async def get_user_profile(websession: aiohttp.ClientSession, access_token: str) -> dict[str, Any]:
        timestamp = (await AuthApi.get_current_time_from_server(websession))["date"]

        async with websession.get(
                "https://kr.lgeapi.com/users/profile",
                headers={
                    "X-Lge-Oauth-Signature": Signature.calculate_signature(f"/users/profile\n{timestamp}"),
                    "X-Lge-Oauth-Date": timestamp,
                    "Authorization": f"Bearer {access_token}",
                    "X-Device-Type": "M01",
                    "X-Device-Platform": "ADR",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "X-Lge-Svccode": "SVC202",
                    "X-Application-Key": APP_KEY,
                    "Lgemp-X-App-Key": APP_KEY,
                    "User-Agent": USER_AGENT_GENERAL,
                }
        ) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return await response.json()

    @staticmethod
    async def get_all_homes(websession: aiohttp.ClientSession, access_token: str, user_no: str) -> list[dict[str, Any]]:
        async with websession.get(
                "https://kic-service.lgthinq.com:46030/v1/service/homes",
                headers={
                    "X-Thinq-App-Ver": APP_VERSION,
                    "X-Thinq-App-Type": "NUTS",
                    "X-Thinq-App-Level": "PRD",
                    "X-Thinq-App-Os": "ANDROID",
                    "X-Service-Code": "SVC202",
                    "X-Country-Code": "KR",
                    "X-Language-Code": "ko-KR",
                    "X-Service-Phase": "OP",
                    "X-Client-Id": CLIENT_ID,
                    "X-Origin": "app-native",
                    "X-Thinq-App-Logintype": "LGE",
                    "X-Model-Name": MODEL_NAME,
                    "X-Os-Version": OS_VERSION,
                    "X-App-Version": APP_VERSION_WITH_APP,
                    "X-Device-Type": "601",
                    "X-User-No": user_no,
                    "X-Api-Key": API_KEY,
                    "Content-Type": "application/json;charset=utf-8",
                    "User-Agent": USER_AGENT_OKHTTP,
                    "Accept": "application/json",
                    "X-Emp-Token": access_token,
                }
        ) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return (await response.json())["result"]["item"]
