class LongFormCountdownCard extends HTMLElement {
  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];
    if (!stateObj) return;

    if (!this.content) {
      this.innerHTML = `
        <ha-card style="padding: 16px;">
          <div id="container" style="display: flex; align-items: center;">
            <ha-icon id="icon" style="margin-right: 16px; --mdc-icon-size: 40px; color: var(--primary-color);"></ha-icon>
            <div>
              <div id="name" style="font-size: 1rem; color: var(--secondary-text-color);"></div>
              <div id="timer" style="font-size: 1.2rem; font-weight: 500; line-height: 1.2;"></div>
            </div>
          </div>
          <style>
            @keyframes blink { 50% { opacity: 0.3; } }
            .flashing { animation: blink 1s linear infinite; color: var(--error-color); }
          </style>
        </ha-card>
      `;
      this.content = this.querySelector("#timer");
      this.nameContainer = this.querySelector("#name");
      this.iconContainer = this.querySelector("#icon");
    }

    let displayState = stateObj.state;

    // Short form logic
    if (this.config.short_form) {
      displayState = displayState
        .replace(/ years?/g, "y")
        .replace(/ months?/g, "m")
        .replace(/ days?/g, "d")
        .replace(/ hours?/g, "h")
        .replace(/ minutes?/g, "m")
        .replace(/ seconds?/g, "s");
    }

    this.nameContainer.innerText = stateObj.attributes.friendly_name;
    this.content.innerText = displayState;
    this.iconContainer.setAttribute("icon", stateObj.attributes.icon || "mdi:timer-sand");

    // Flash logic based on card config + sensor state
    const isFinished = stateObj.state.includes("Elapsed") || stateObj.attributes.total_seconds_left <= 0;
    if (this.config.flash_zero && isFinished) {
      this.content.classList.add("flashing");
    } else {
      this.content.classList.remove("flashing");
    }
  }

  setConfig(config) {
    if (!config.entity) throw new Error("Define an entity");
    this.config = config;
  }

  // Visual Editor Support
  static getStubConfig() {
    return { entity: "", short_form: false, flash_zero: false };
  }
}
customElements.define("long-form-countdown-card", LongFormCountdownCard);
