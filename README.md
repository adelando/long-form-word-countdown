# ⏳ Long Form Word Countdown (LFWC)

A professional Home Assistant integration that provides highly descriptive countdown timers. Instead of simple timestamps, get a detailed breakdown in plain English (Years, Months, Days, etc.) with a dedicated custom dashboard card.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

## ✨ Features
- **Visual Card Editor:** Configure your countdowns via a native UI—no YAML required.
- **Prefix Organization:** All entities are automatically prefixed with `lfwc_` for easy filtering.
- **Smart Grammar:** Correctly handles pluralization (e.g., "1 day" vs "2 days").
- **Short Form Toggle:** Instantly switch between "1 year, 2 months" and "1y, 2m" via the card settings.
- **Elapsed Tracking:** Automatically switches to "Elapsed" mode once the target date passes.
- **Flash on Zero:** Optional visual alert that blinks the card when the timer expires.



## 🚀 Installation

### 1. HACS (Recommended)
1. Open **HACS** > **Integrations**.
2. Click the three dots (top right) > **Custom repositories**.
3. Add this Repository URL with the category **Integration**.
4. Click **Install**, then **Restart Home Assistant**.

### 2. Manual
1. Copy the `long_form_word_countdown` folder into your `custom_components` directory.
2. Restart Home Assistant.

## 🛠 Setup

### Integration Setup
1. Go to **Settings** > **Devices & Services** > **Add Integration**.
2. Search for **Long Form Word Countdown**.
3. Enter your event name and target date. 
   * *Note: Your entity will be created as `sensor.lfwc_your_name`.*
Note: The sensor will use local machine time for the countdown.

### Dashboard Card Setup
1. Go to your Dashboard and click **Edit Dashboard** > **Add Card**.
2. Search for **Long Form Word Countdown Card**.
3. Use the visual editor to:
   - Select your `lfwc_` sensor.
   - Toggle **Short Form** (y, m, d) vs **Long Form** (years, months, days).
   - Enable **Flash on Zero** if you want a visual alert for finished timers.
   - Enable **Elapse timer** 



## 📁 Repository Structure
```text
custom_components/long_form_word_countdown/
├── translations/   # UI Text
├── www/            # Custom Card & Visual Editor
├── __init__.py     # Async Path Registration
├── config_flow.py  # Integration UI
├── manifest.json   # Dependencies & Versioning
└── sensor.py       # Precise Math Engine
