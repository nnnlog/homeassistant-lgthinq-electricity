import os
from typing import Any

import aiohttp

from .const import CLIENT_ID, MODEL_NAME, OS_VERSION, APP_VERSION_WITH_APP, APP_KEY, \
    USER_AGENT_GENERAL, APP_VERSION, API_KEY, USER_AGENT_OKHTTP
from ..model.exception import UnauthorizedException


class DeviceApi:
    @staticmethod
    async def get_all_devices(websession: aiohttp.ClientSession, access_token: str, user_no: str, home_id: str) -> list[
        dict[str, Any]]:
        async with websession.get(
                f"https://kic-service.lgthinq.com:46030/v1/service/homes/{home_id}",
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
                    "X-Message-Id": os.urandom(16).hex(),
                }
        ) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return (await response.json())["result"]["devices"]

    @staticmethod
    async def get_device_energy_history_aircon(
            websession: aiohttp.ClientSession, access_token: str, user_no: str, device_id: str, start_date: str,
            end_date: str, period: str
    ) -> list[dict[str, Any]]:
        async with websession.get(
                f"https://kic-service.lgthinq.com:46030/v1/service/aircon/{device_id}/energy-history?period={period}&startDate={start_date}&endDate={end_date}&saveEnergyYn=Y",
                headers={
                    "X-Thinq-App-Type": "NUTS",
                    "X-Thinq-App-Ver": APP_VERSION,
                    "X-Api-Key": API_KEY,
                    "X-Thinq-App-Logintype": "LGE",
                    "X-Origin": "app-web-ANDROID",
                    "X-Country-Code": "KR",
                    "Accept": "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                    "X-Client-Id": CLIENT_ID,
                    "X-User-No": user_no,
                    "Cache-Control": "no-cache",
                    "X-Message-Id": os.urandom(16).hex(),
                    "X-Language-Code": "ko-KR",
                    "X-Service-Code": "SVC202",
                    "X-Thinq-App-Level": "PRD",
                    "X-Service-Phase": "OP",
                    "X-App-Version": APP_VERSION_WITH_APP,
                    "User-Agent": USER_AGENT_GENERAL,
                    "X-Thinq-App-Os": "ANDROID",
                    "X-Emp-Token": access_token,
                    "X-Thinq-App-Pageid": "GJM_ENM01_Moment/002",
                    "X-Requested-With": "com.lgeha.nuts",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Priority": "u=1, i",
                }) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return (await response.json())["result"]

    @staticmethod
    async def get_device_energy_history_laundry(
            websession: aiohttp.ClientSession, access_token: str, user_no: str, device_id: str, start_date: str,
            end_date: str, period: str
    ) -> list[dict[str, Any]]:
        async with websession.get(
                f"https://kic-service.lgthinq.com:46030/v1/service/laundry/{device_id}/energy-history?type=period&period={period}&startDate={start_date}&endDate={end_date}",
                headers={
                    "X-Thinq-App-Type": "NUTS",
                    "X-Thinq-App-Ver": APP_VERSION,
                    "X-Api-Key": API_KEY,
                    "X-Thinq-App-Logintype": "LGE",
                    "X-Origin": "app-web-ANDROID",
                    "X-Country-Code": "KR",
                    "Accept": "application/json",
                    "Content-Type": "application/json;charset=UTF-8",
                    "X-Client-Id": CLIENT_ID,
                    "X-User-No": user_no,
                    "Cache-Control": "no-cache",
                    "X-Message-Id": os.urandom(16).hex(),
                    "X-Language-Code": "ko-KR",
                    "X-Service-Code": "SVC202",
                    "X-Thinq-App-Level": "PRD",
                    "X-Service-Phase": "OP",
                    "X-App-Version": APP_VERSION_WITH_APP,
                    "User-Agent": USER_AGENT_GENERAL,
                    "X-Thinq-App-Os": "ANDROID",
                    "X-Emp-Token": access_token,
                    "X-Thinq-App-Pageid": "GWM_ENM01_Main/201",
                    "X-Requested-With": "com.lgeha.nuts",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Priority": "u=1, i",
                }) as response:
            if response.status == 400:
                raise UnauthorizedException()
            response.raise_for_status()
            return (await response.json())["result"]["item"]
