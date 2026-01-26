import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register the JS card path using the modern async method
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        # The new API call for recent HA versions
        await hass.http.async_register_static_paths([
            hass.http.StaticPathConfig("/long_form_word_countdown", local_path, True)
        ])
    else:
        _LOGGER.warning("The www directory was not found in the integration folder")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
