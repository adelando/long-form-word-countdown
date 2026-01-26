class LongFormCountdownCard extends HTMLElement {
  set hass(hass) {
    const stateObj = hass.states[this.config.entity];
    if (!stateObj) return;

    const finished = stateObj.attributes.finished;
    const flashEnabled = stateObj.attributes.flash_zero;

    if (!this.content) {
      this.innerHTML = `
        <ha-card style="padding: 20px; text-align: center;">
          <div id="name" style="font-size: 1.1em; opacity: 0.7;"></div>
          <div id="timer" style="font-size: 1.8em; font-weight: bold; margin-top: 10px;"></div>
          <style>
            @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
            .flashing { animation: blink 1s linear infinite; color: var(--error-color); }
          </style>
        </ha-card>
      `;
      this.content = this.querySelector("#timer");
      this.nameContainer = this.querySelector("#name");
    }

    this.nameContainer.innerText = stateObj.attributes.friendly_name;
    this.content.innerText = stateObj.state;
    
    if (finished && flashEnabled) {
      this.content.classList.add("flashing");
    } else {
      this.content.classList.remove("flashing");
    }
  }

  setConfig(config) {
    this.config = config;
  }
}
customElements.define("long-form-countdown-card", LongFormCountdownCard);
