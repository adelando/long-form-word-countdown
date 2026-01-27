from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CONF_TARGET_DATE

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([LongFormCountdownSensor(entry)], True)

class LongFormCountdownSensor(SensorEntity):
    _attr_should_poll = False
    _attr_has_entity_name = True
    # Setting force_update to False prevents unnecessary database writes
    _attr_force_update = False 

    def __init__(self, entry):
        self._entry = entry
        clean_name = entry.data["name"].lower().replace(" ", "_")
        self.entity_id = f"sensor.lfwc_{clean_name}"
        self._attr_unique_id = f"lfwc_{entry.entry_id}"
        self._attr_name = entry.data["name"]
        
        self._target_date = dt_util.as_local(datetime.fromisoformat(entry.data[CONF_TARGET_DATE]))
        self._attr_icon = entry.data.get("icon", "mdi:timer-sand")
        
        self._state = None
        self._finished = False

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {
            "finished": self._finished,
            "total_seconds_left": (self._target_date - dt_util.now()).total_seconds()
        }

    async def async_added_to_hass(self):
        await self._update_and_schedule()

    async def _update_and_schedule(self, _=None):
        now = dt_util.now()
        is_past = now >= self._target_date
        self._finished = is_past

        start, end = (self._target_date, now) if is_past else (now, self._target_date)
        diff = relativedelta(end, start)
        
        parts = []
        if diff.years: parts.append(f"{diff.years} {'year' if diff.years == 1 else 'years'}")
        if diff.months: parts.append(f"{diff.months} {'month' if diff.months == 1 else 'months'}")
        if diff.days: parts.append(f"{diff.days} {'day' if diff.days == 1 else 'days'}")
        if diff.hours: parts.append(f"{diff.hours} {'hour' if diff.hours == 1 else 'hours'}")
        if diff.minutes: parts.append(f"{diff.minutes} {'minute' if diff.minutes == 1 else 'minutes'}")
        if diff.seconds: parts.append(f"{diff.seconds} {'second' if diff.seconds == 1 else 'seconds'}")
        
        output = ", ".join(parts) if parts else "0 seconds"
        self._state = f"Elapsed: {output}" if is_past else output

        self.async_write_ha_state()

        # Schedule the next tick
        next_update = now + timedelta(seconds=1)
        async_track_point_in_time(self.hass, self._update_and_schedule, next_update)
