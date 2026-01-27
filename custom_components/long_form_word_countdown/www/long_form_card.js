class LongFormCountdownCard extends HTMLElement {
  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];
    if (!stateObj) return;

    if (!this.content) {
      this.innerHTML = `
        <ha-card style="padding: 16px;">
          <div id="container" style="display: flex; align-items: center;">
            <ha-icon id="icon" style="margin-right: 16px; --mdc-icon-size: 40px;"></ha-icon>
            <div style="flex: 1;">
              <div id="name" style="font-size: 0.9rem; color: var(--secondary-text-color); font-weight: 500;"></div>
              <div id="timer" style="line-height: 1.3;"></div>
            </div>
          </div>
          <style>
            @keyframes blink { 50% { opacity: 0.3; } }
            .flashing { animation: blink 1s linear infinite; color: var(--error-color) !important; font-weight: bold; }
          </style>
        </ha-card>
      `;
      this.content = this.querySelector("#timer");
      this.nameContainer = this.querySelector("#name");
      this.iconContainer = this.querySelector("#icon");
    }

    let displayState = stateObj.state;
    const isFinished = stateObj.attributes.finished || stateObj.attributes.total_seconds_left <= 0;

    if (isFinished) {
      if (this.config.flash_zero) {
        displayState = "Timer Complete";
      } else if (!this.config.show_elapsed) {
        displayState = "0 seconds";
      }
    }

    if (this.config.short_form) {
      displayState = displayState
        .replace(/ years?/g, "y").replace(/ months?/g, "m").replace(/ days?/g, "d")
        .replace(/ hours?/g, "h").replace(/ minutes?/g, "m").replace(/ seconds?/g, "s");
    }

    // Apply Theme Styles
    const timerColor = this.config.timer_color || 'var(--primary-color)';
    const fontSize = this.config.font_size || '1.1';
    
    this.content.style.color = timerColor;
    this.content.style.fontSize = `${fontSize}rem`;
    this.iconContainer.style.color = timerColor;

    this.nameContainer.innerText = stateObj.attributes.friendly_name;
    this.content.innerText = displayState;
    this.iconContainer.setAttribute("icon", stateObj.attributes.icon || "mdi:timer-sand");

    if (this.config.flash_zero && isFinished) {
      this.content.classList.add("flashing");
    } else {
      this.content.classList.remove("flashing");
    }
  }

  setConfig(config) {
    this.config = { 
      short_form: false, 
      flash_zero: false, 
      show_elapsed: true, 
      timer_color: "", 
      font_size: "1.1",
      ...config 
    };
  }

  static getConfigElement() { return document.createElement("long-form-countdown-editor"); }
  static getStubConfig() { return { entity: "", short_form: false, flash_zero: false, show_elapsed: true }; }
}

// --- VISUAL EDITOR WITH THEME OPTIONS ---
class LongFormCountdownEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (this._config) this._render();
  }
  setConfig(config) { this._config = config; }

  _render() {
    if (this.shadowRoot) this.shadowRoot.innerHTML = "";
    else this.attachShadow({ mode: "open" });

    const container = document.createElement("div");
    container.innerHTML = `
      <style>
        .option { padding: 12px 0; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--divider-color); }
        .theme-section { margin-top: 15px; padding: 10px; background: var(--secondary-background-color); border-radius: 8px; }
        .label { font-weight: bold; margin-bottom: 8px; display: block; }
        input[type="color"] { border: none; width: 30px; height: 30px; cursor: pointer; background: none; }
      </style>
      
      <ha-entity-picker .label="Countdown Entity" .hass=${this._hass} .value=${this._config.entity} .includeDomains=${["sensor"]} @value-changed=${(ev) => this._valueChanged(ev, "entity")}></ha-entity-picker>
      
      <div class="option"><span>Short Form (y, m, d)</span>
        <ha-switch .checked=${this._config.short_form} @change=${(ev) => this._valueChanged(ev, "short_form", true)}></ha-switch>
      </div>
      <div class="option"><span>Show Elapsed Time</span>
        <ha-switch .checked=${this._config.show_elapsed} @change=${(ev) => this._toggleExclusive(ev, "show_elapsed")}></ha-switch>
      </div>
      <div class="option"><span>Flash "Timer Complete"</span>
        <ha-switch .checked=${this._config.flash_zero} @change=${(ev) => this._toggleExclusive(ev, "flash_zero")}></ha-switch>
      </div>

      <div class="theme-section">
        <span class="label">Theme Settings</span>
        <div class="option">
          <span>Timer Color</span>
          <input type="color" .value=${this._config.timer_color || "#3498db"} @input=${(ev) => this._valueChanged(ev, "timer_color")}>
        </div>
        <div class="option">
          <span>Font Size (rem)</span>
          <input type="range" min="0.8" max="2.5" step="0.1" .value=${this._config.font_size || "1.1"} @input=${(ev) => this._valueChanged(ev, "font_size")}>
        </div>
      </div>
    `;
    this.shadowRoot.appendChild(container);
  }

  _toggleExclusive(ev, field) {
    const isChecked = ev.target.checked;
    let newConfig = { ...this._config, [field]: isChecked };
    if (field === "show_elapsed" && isChecked) newConfig.flash_zero = false;
    if (field === "flash_zero" && isChecked) newConfig.show_elapsed = false;
    this._config = newConfig;
    this._render();
    this._fireConfigChanged();
  }

  _valueChanged(ev, field, isBoolean = false) {
    const val = isBoolean ? ev.target.checked : (ev.detail ? ev.detail.value : ev.target.value);
    this._config = { ...this._config, [field]: val };
    this._fireConfigChanged();
  }

  _fireConfigChanged() {
    this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: this._config }, bubbles: true, composed: true }));
  }
}

customElements.define("long-form-countdown-card", LongFormCountdownCard);
customElements.define("long-form-countdown-editor", LongFormCountdownEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "long-form-countdown-card",
  name: "Long Form Word Countdown",
  preview: true,
});
