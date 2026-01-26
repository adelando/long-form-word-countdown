import os
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register the 'www' directory so the JS card is accessible
    hass.http.register_static_path(
        "/long_form_word_countdown",
        hass.config.path("custom_components/long_form_word_countdown/www"),
        True
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
