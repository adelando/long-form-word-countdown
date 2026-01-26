import os
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})
    
    # Corrected static path registration
    # This maps 'http://your-ha-ip:8123/long_form_word_countdown/long-form-card.js'
    # to your local www folder
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        hass.http.register_static_path(
            "/long_form_word_countdown",
            local_path,
            cache_headers=False
        )
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
