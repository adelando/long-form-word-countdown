import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig

_LOGGER = logging.getLogger(__name__)
DOMAIN = "long_form_word_countdown"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    
    # 1. Register the static path
    # We use a very simple name 'lfwc' for the URL
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        await hass.http.async_register_static_paths([
            StaticPathConfig("/lfwc", local_path, False)
        ])
        
        # 2. Add the URL to the frontend
        # Note: We add a version query (?v=1) to force the browser to stop caching old errors
        add_extra_js_url(hass, "/lfwc/long-form-card.js?v=1")
        _LOGGER.info("LFWC Card registered at /lfwc/long-form-card.js")
    else:
        _LOGGER.error("FOLDER NOT FOUND: %s", local_path)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
