from homeassistant.const import Platform

DOMAIN = "lgthinqelectricity"

CONF_REFRESH_TOKEN = "refresh_token"
CONF_ACCESS_TOKEN = "access_token"
CONF_USER_ID = "user_id"
CONF_USER_NO = "user_no"
CONF_HOME_ID = "home_id"

PLATFORMS = [Platform.SENSOR]
