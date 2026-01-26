from datetime import datetime
from dateutil.relativedelta import relativedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

from .const import DOMAIN, CONF_TARGET_DATE

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([LongFormCountdownSensor(entry)], True)

class LongFormCountdownSensor(SensorEntity):
    """Representation of a Countdown Sensor."""

    def __init__(self, entry):
        self._entry = entry
        self._attr_name = entry.data["name"]
        self._attr_unique_id = f"{entry.entry_id}_countdown"
        self._target_date = datetime.fromisoformat(entry.data[CONF_TARGET_DATE])
        self._attr_icon = entry.data.get("icon", "mdi:timer-sand")
        self._state = None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_added_to_hass(self):
        """Register update listener."""
        self.async_on_remove(
            async_track_time_interval(self.hass, self.async_update_state, timedelta(seconds=1))
        )

    async def async_update_state(self, _=None):
        """Calculate the remaining time."""
        now = datetime.now()
        
        if now >= self._target_date:
            self._state = "Completed"
        else:
            diff = relativedelta(self._target_date, now)
            
            parts = []
            if diff.years: parts.append(f"{diff.years}y")
            if diff.months: parts.append(f"{diff.months}m")
            if diff.days: parts.append(f"{diff.days}d")
            if diff.hours: parts.append(f"{diff.hours}h")
            if diff.minutes: parts.append(f"{diff.minutes}m")
            if diff.seconds: parts.append(f"{diff.seconds}s")
            
            self._state = ", ".join(parts)
        
        self.async_write_ha_state()