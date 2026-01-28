import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})

    # 1. Automate the folder mapping
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        # This maps your internal folder to /lfwc-files/ so HA can see it
        await hass.http.async_register_static_paths([
            StaticPathConfig("/lfwc-files", local_path, False)
        ])
        
        # 2. Automate the Resource Registration
        # This 'injects' the card into the dashboard automatically
        add_extra_js_url(hass, "/lfwc-files/long-form-card.js")
    else:
        _LOGGER.error("The www directory was not found at %s", local_path)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
