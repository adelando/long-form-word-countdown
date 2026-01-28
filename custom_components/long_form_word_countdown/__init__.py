import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 1. Identify the internal path
    js_dir = hass.config.path("custom_components/long_form_word_countdown/www")
    js_file = os.path.join(js_dir, "long-form-card.js")
    
    _LOGGER.warning("LFWC: Checking for folder at: %s", js_dir)

    # 2. Check if folder and file actually exist
    if os.path.exists(js_dir):
        _LOGGER.warning("LFWC: Folder FOUND. Registering URL path /lfwc-card/")
        
        await hass.http.async_register_static_paths([
            StaticPathConfig("/lfwc-card", js_dir, False)
        ])
        
        if os.path.isfile(js_file):
             _LOGGER.warning("LFWC: JS file FOUND. Adding to frontend.")
             # v=101 to force a fresh download
             add_extra_js_url(hass, "/lfwc-card/long-form-card.js?v=101")
        else:
             _LOGGER.warning("LFWC: JS file NOT FOUND at %s", js_file)
    else:
        _LOGGER.warning("LFWC: Folder NOT FOUND at %s", js_dir)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
