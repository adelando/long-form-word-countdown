import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import (
    DateTimeSelector,
    IconSelector,
    TextSelector,
)
from .const import DOMAIN, CONF_TARGET_DATE

class LongFormCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Long Form Word Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"], 
                data=user_input
            )

        # Define the UI Schema
        data_schema = vol.Schema({
            vol.Required("name"): TextSelector(),
            vol.Required(CONF_TARGET_DATE): DateTimeSelector(),
            vol.Optional("icon", default="mdi:timer-sand"): IconSelector(),
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )