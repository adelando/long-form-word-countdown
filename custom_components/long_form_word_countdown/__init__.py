import logging
import os
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Get the absolute path to your www folder inside the integration
    # This path MUST exist: custom_components/long_form_word_countdown/www/
    js_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(js_path):
        _LOGGER.warning("LFWC: Registering static path at %s", js_path)
        await hass.http.async_register_static_paths([
            StaticPathConfig("/lfwc-card", js_path, False)
        ])
        # We use a unique version number to kill the cache
        add_extra_js_url(hass, "/lfwc-card/long-form-card.js?v=999")
    else:
        _LOGGER.error("LFWC: Could not find www folder at %s", js_path)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
