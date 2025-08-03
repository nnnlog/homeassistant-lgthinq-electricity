from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator


class LgThinqEntity(CoordinatorEntity[dict[str, Any]], SensorEntity):
    device_id: str

    def __init__(self, coordinator: DataUpdateCoordinator[dict[str, Any]], entity_description: EntityDescription,
                 device_id: str):
        super().__init__(coordinator)

        self.unique_id = f"{coordinator.config_entry.unique_id}_{device_id}_{entity_description.key}"
        self.entity_description = entity_description
        self.device_id = device_id

        data = coordinator.data[device_id]
        self._attr_name = data["name"]
        self._attr_device_info = data["info"]
        self._attr_native_value = data["value"]

    @property
    def available(self) -> bool:
        """Return True if the entity is available."""
        return self.coordinator.last_update_success and self._data is not None

    @property
    def _data(self):
        """Return the data for this entity."""
        return self.coordinator.data.get(self.device_id, None)

    @callback
    def _handle_coordinator_update(self):
        """Handle updated data from the coordinator."""
        data = self._data
        self._attr_native_value = data["value"]

        super()._handle_coordinator_update()