import logging
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)
DOMAIN = "long_form_word_countdown"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""

    # 1. Map the internal folder to a web-accessible URL path
    # This makes 'custom_components/long_form_word_countdown/www' 
    # visible at the URL: '/lfwc-card'
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            "/lfwc-card", 
            hass.config.path("custom_components/long_form_word_countdown/www"), 
            False
        )
    ])

    # 2. Tell the dashboard to load the JS file from that new path
    # We add a version ?v=1 to ensure it refreshes
    add_extra_js_url(hass, "/lfwc-card/long-form-card.js?v=1")

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
