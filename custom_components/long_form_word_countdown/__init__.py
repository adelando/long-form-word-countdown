import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    
    # 1. Map the folder so it's accessible via URL
    # This makes /config/custom_components/long_form_word_countdown/www/ 
    # visible at the URL: /lfwc-card/
    dist_dir = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(dist_dir):
        await hass.http.async_register_static_paths([
            StaticPathConfig("/lfwc-card", dist_dir, False)
        ])
        
        # 2. Tell the dashboard to load the file automatically
        # This replaces the need for a manual entry in the Resource Manager
        add_extra_js_url(hass, "/lfwc-card/long-form-card.js")
    
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
