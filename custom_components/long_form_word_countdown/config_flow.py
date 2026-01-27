import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN, CONF_TARGET_DATE

class LongFormCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Long Form Word Countdown."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): selector.TextSelector(),
                vol.Required(CONF_TARGET_DATE): selector.DateTimeSelector(),
                vol.Optional("icon", default="mdi:timer-sand"): selector.IconSelector(),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return LongFormCountdownOptionsFlowHandler(config_entry)

class LongFormCountdownOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for the integration (The 'Configure' button)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Update the entry data with the new values
            new_data = {**self.config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("name", default=self.config_entry.data.get("name")): selector.TextSelector(),
                vol.Required(CONF_TARGET_DATE, default=self.config_entry.data.get(CONF_TARGET_DATE)): selector.DateTimeSelector(),
                vol.Optional("icon", default=self.config_entry.data.get("icon", "mdi:timer-sand")): selector.IconSelector(),
            })
        )
