from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class LgThinqConfig:
    refresh_token: str
    user_no: str
    home_id: str

    unique_id: str

    def __init__(self, refresh_token: str, user_no: str, home_id: str, unique_id: str):
        self.refresh_token = refresh_token
        self.user_no = user_no
        self.home_id = home_id

        self.unique_id = unique_id


class LgThinqConfigEntryRuntimeData:
    config: LgThinqConfig

    access_token: str = ""
    coordinator: DataUpdateCoordinator
