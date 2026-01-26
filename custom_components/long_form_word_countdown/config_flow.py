import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_TARGET_DATE, CONF_AFTER_TIMER, CONF_FLASH_ZERO

class LongFormCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Long Form Word Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Logic check: both cannot be True
            if user_input.get(CONF_AFTER_TIMER) and user_input.get(CONF_FLASH_ZERO):
                errors["base"] = "cannot_select_both"
            else:
                return self.async_create_entry(
                    title=user_input["name"], 
                    data=user_input
                )

        # Updated schema with specific selectors
        data_schema = vol.Schema({
            vol.Required("name"): selector.TextSelector(),
            vol.Required(CONF_TARGET_DATE): selector.DateTimeSelector(),
            vol.Optional("icon", default="mdi:timer-sand"): selector.IconSelector(),
            vol.Optional(CONF_AFTER_TIMER, default=True): selector.BooleanSelector(),
            vol.Optional(CONF_FLASH_ZERO, default=False): selector.BooleanSelector(),
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )
