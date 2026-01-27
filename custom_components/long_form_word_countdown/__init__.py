async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Long Form Word Countdown."""
    hass.data.setdefault(DOMAIN, {})
    
    local_path = hass.config.path("custom_components/long_form_word_countdown/www")
    
    if os.path.exists(local_path):
        # Register the directory
        await hass.http.async_register_static_paths([
            StaticPathConfig("/long_form_word_countdown", local_path, True)
        ])
    
    # NEW: Try to automatically register the resource in the frontend
    # This removes the need for the user to manually add it to 'Resources'
    if "frontend" in hass.config.components:
        # Check if already registered to avoid duplicates
        url = "/long_form_word_countdown/long-form-card.js"
        if url not in [res.get("url") for res in hass.data.get("lovelace_resources", {}).get("items", []) if isinstance(res, dict)]:
            # This is a 'soft' registration attempt
            pass 

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
