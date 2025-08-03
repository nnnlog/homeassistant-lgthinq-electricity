from homeassistant.components.sensor import SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .lib.homeassistant.lg_thinq_entity import LgThinqEntity
from .lib.model.config import LgThinqConfigEntryRuntimeData

DESCRIPTIONS = [
    SensorEntityDescription(
        key="value",
        translation_key="electricity",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement="kWh",
        has_entity_name=True,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[LgThinqConfigEntryRuntimeData],
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities: list[Entity] = []

    coordinator = entry.runtime_data.coordinator
    for device_id, data in coordinator.data.items():
        for description in DESCRIPTIONS:
            if description.key not in data:
                continue

            entities.append(LgThinqEntity(coordinator, description, device_id))

    async_add_entities(entities)
