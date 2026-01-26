# ⏳ Long Form Word Countdown for Home Assistant

A custom Home Assistant integration that provides a highly descriptive countdown timer. Instead of just showing "3 days," it provides a detailed "Long Form" breakdown including years, months, days, hours, minutes, and seconds.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

## ✨ Features
* **UI Configuration:** No YAML required! Add and configure via the Integrations menu.
* **Detailed Breakdown:** Shows time remaining in `Y, M, D, H, M, S` format.
* **Smart Formatting:** Automatically hides units that are zero (e.g., won't show "0y" if the date is this month).
* **Custom Icons:** Choose any Material Design Icon during setup to match your event.
* **Live Updates:** The sensor updates every second for precision.

## 🚀 Installation

### Option 1: HACS (Recommended)
1.  Open **HACS** in Home Assistant.
2.  Click the three dots in the top right and select **Custom repositories**.
3.  Paste the URL of this repository: `https://github.com/adelando/long-form-word-countdown`.
4.  Select **Integration** as the category and click **Add**.
5.  Click **Install**.
6.  Restart Home Assistant.

### Option 2: Manual
1.  Download the `long_form_word_countdown` folder from `custom_components/`.
2.  Paste it into your Home Assistant `/config/custom_components/` directory.
3.  Restart Home Assistant.

## 🛠 Setup
1.  Go to **Settings** > **Devices & Services**.
2.  Click **+ Add Integration**.
3.  Search for **Long Form Word Countdown**.
4.  Follow the prompts to enter:
    * **Name:** (e.g., "Summer Holiday")
    * **Target Date & Time:** Use the calendar and clock picker.
    * **Icon:** (e.g., `mdi:beach`)

## 📊 Dashboard Example
For a clean "Big Text" look, use a **Markdown Card**:

```yaml
type: markdown
content: >
  # {{ state_attr('sensor.summer_holiday', 'friendly_name') }}
  ### {{ states('sensor.summer_holiday') }}
