from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CONF_TARGET_DATE, CONF_AFTER_TIMER, CONF_FLASH_ZERO

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    async_add_entities([LongFormCountdownSensor(entry)], True)

class LongFormCountdownSensor(SensorEntity):
    """Representation of a Long Form Word Countdown sensor."""

    def __init__(self, entry):
        self._entry = entry
        self._attr_name = entry.data["name"]
        self._attr_unique_id = f"{entry.entry_id}_countdown"
        self._target_date = dt_util.as_local(datetime.fromisoformat(entry.data[CONF_TARGET_DATE]))
        self._after_timer = entry.data.get(CONF_AFTER_TIMER, True)
        self._flash_zero = entry.data.get(CONF_FLASH_ZERO, False)
        self._attr_icon = entry.data.get("icon", "mdi:timer-sand")
        self._state = None
        self._finished = False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return {
            "finished": self._finished,
            "flash_zero": self._flash_zero,
            "target_date": self._target_date.isoformat()
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await self._update_and_schedule()

    async def _update_and_schedule(self, _=None):
        """Update state and schedule next update."""
        now = dt_util.now()
        is_past = now >= self._target_date
        self._finished = is_past

        # Logic for state string
        if is_past and not self._after_timer:
            self._state = "Timer Complete"
        else:
            # Calculate difference
            start, end = (self._target_date, now) if is_past else (now, self._target_date)
            diff = relativedelta(end, start)
            
            parts = []
            if diff.years: parts.append(f"{diff.years}y")
            if diff.months: parts.append(f"{diff.months}m")
            if diff.days: parts.append(f"{diff.days}d")
            if diff.hours: parts.append(f"{diff.hours}h")
            if diff.minutes: parts.append(f"{diff.minutes}m")
            if diff.seconds: parts.append(f"{diff.seconds}s")
            
            time_str = ", ".join(parts) if parts else "0s"
            self._state = f"Elapsed: {time_str}" if is_past else time_str

        self.async_write_ha_state()

        # Schedule next update in exactly 1 second
        next_update = now + timedelta(seconds=1)
        async_track_point_in_time(self.hass, self._update_and_schedule, next_update)
