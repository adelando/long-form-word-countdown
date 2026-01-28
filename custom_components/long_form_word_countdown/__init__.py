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

    # 1. Map the internal folder to a URL path (Modern Async Way)
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        # The new API expects a list of StaticPathConfig objects
        await hass.http.async_register_static_paths([
            StaticPathConfig("/long_form_word_countdown", local_path, False)
        ])
        
        # 2. Automatically register the JS as a Lovelace resource
        js_url = "/long_form_word_countdown/long-form-card.js"
        add_extra_js_url(hass, js_url)
        _LOGGER.debug("Registered and injected JS resource: %s", js_url)
    else:
        _LOGGER.error("The www directory was not found at %s", local_path)

    # 3. Register the listener for the 'Configure' button updates
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the integration when options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
