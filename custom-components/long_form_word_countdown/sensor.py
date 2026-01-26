from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, CONF_TARGET_DATE, CONF_AFTER_TIMER

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([LongFormCountdownSensor(entry)], True)

class LongFormCountdownSensor(SensorEntity):
    def __init__(self, entry):
        self._entry = entry
        self._attr_name = entry.data["name"]
        self._attr_unique_id = f"{entry.entry_id}_countdown"
        self._target_date = datetime.fromisoformat(entry.data[CONF_TARGET_DATE])
        self._after_timer = entry.data.get(CONF_AFTER_TIMER, True)
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
            "flash_zero": self._entry.data.get("flash_zero", False)
        }

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(self.hass, self.async_update_state, timedelta(seconds=1))
        )

    async def async_update_state(self, _=None):
        now = datetime.now()
        is_past = now >= self._target_date
        self._finished = is_past

        if is_past and not self._after_timer:
            self._state = "Timer Complete"
        else:
            start, end = (self._target_date, now) if is_past else (now, self._target_date)
            diff = relativedelta(end, start)
            
            p = []
            if diff.years: p.append(f"{diff.years}y")
            if diff.months: p.append(f"{diff.months}m")
            if diff.days: p.append(f"{diff.days}d")
            if diff.hours: p.append(f"{diff.hours}h")
            if diff.minutes: p.append(f"{diff.minutes}m")
            if diff.seconds: p.append(f"{diff.seconds}s")
            
            time_str = ", ".join(p) if p else "0s"
            self._state = f"Elapsed: {time_str}" if is_past else time_str
        
        self.async_write_ha_state()
