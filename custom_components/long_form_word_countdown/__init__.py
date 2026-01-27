import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})
    
    # Path to the www folder containing the JS card
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        # Register the static path so the JS is accessible via URL
        await hass.http.async_register_static_paths([
            StaticPathConfig("/long_form_word_countdown", local_path, True)
        ])
        _LOGGER.debug("Long Form Word Countdown: Static path registered successfully")
    else:
        _LOGGER.error("Long Form Word Countdown: The www directory was not found at %s", local_path)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
