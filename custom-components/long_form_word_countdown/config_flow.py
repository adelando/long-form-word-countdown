import vol
from homeassistant import config_entries
from homeassistant.helpers.selector import DateTimeSelector, IconSelector, TextSelector, BooleanSelector
from .const import DOMAIN, CONF_TARGET_DATE, CONF_AFTER_TIMER, CONF_FLASH_ZERO

class LongFormCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if user_input.get(CONF_AFTER_TIMER) and user_input.get(CONF_FLASH_ZERO):
                errors["base"] = "cannot_select_both"
            else:
                return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("name"): TextSelector(),
            vol.Required(CONF_TARGET_DATE): DateTimeSelector(),
            vol.Optional("icon", default="mdi:timer-sand"): IconSelector(),
            vol.Optional(CONF_AFTER_TIMER, default=True): BooleanSelector(),
            vol.Optional(CONF_FLASH_ZERO, default=False): BooleanSelector(),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
