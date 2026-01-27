class LongFormCountdownCard extends HTMLElement {
  // --- MAIN CARD LOGIC ---
  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];
    if (!stateObj) return;

    if (!this.content) {
      this.innerHTML = `
        <ha-card style="padding: 16px;">
          <div id="container" style="display: flex; align-items: center;">
            <ha-icon id="icon" style="margin-right: 16px; --mdc-icon-size: 40px; color: var(--primary-color);"></ha-icon>
            <div style="flex: 1;">
              <div id="name" style="font-size: 0.9rem; color: var(--secondary-text-color); font-weight: 500;"></div>
              <div id="timer" style="font-size: 1.1rem; font-weight: 400; line-height: 1.3;"></div>
            </div>
          </div>
          <style>
            @keyframes blink { 50% { opacity: 0.3; } }
            .flashing { animation: blink 1s linear infinite; color: var(--error-color); font-weight: bold; }
          </style>
        </ha-card>
      `;
      this.content = this.querySelector("#timer");
      this.nameContainer = this.querySelector("#name");
      this.iconContainer = this.querySelector("#icon");
    }

    let displayState = stateObj.state;

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

    const isFinished = stateObj.state.includes("Elapsed") || stateObj.attributes.total_seconds_left <= 0;
    if (this.config.flash_zero && isFinished) {
      this.content.classList.add("flashing");
    } else {
      this.content.classList.remove("flashing");
    }
  }

  setConfig(config) {
    this.config = config;
  }

  // Tells Home Assistant to use the custom editor
  static getConfigElement() {
    return document.createElement("long-form-countdown-editor");
  }

  static getStubConfig() {
    return { entity: "", short_form: false, flash_zero: false };
  }
}

// --- VISUAL EDITOR LOGIC ---
class LongFormCountdownEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (this._config) this._updateEditor();
  }

  setConfig(config) {
    this._config = config;
  }

  connectedCallback() {
    this._updateEditor();
  }

  _updateEditor() {
    if (this.shadowRoot) return; // Only build once

    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <div class="card-config">
        <ha-entity-picker
          .label="Select Countdown Entity"
          .hass=${this._hass}
          .value=${this._config.entity}
          .includeDomains=${['sensor']}
          @value-changed=${(ev) => this._valueChanged(ev, 'entity')}
        ></ha-entity-picker>
        
        <div style="margin-top: 20px;">
          <ha-formfield label="Short Form (y, m, d)">
            <ha-switch
              .checked=${this._config.short_form}
              @change=${(ev) => this._valueChanged(ev, 'short_form', true)}
            ></ha-switch>
          </ha-formfield>
        </div>

        <div style="margin-top: 10px;">
          <ha-formfield label="Flash on Zero">
            <ha-switch
              .checked=${this._config.flash_zero}
              @change=${(ev) => this._valueChanged(ev, 'flash_zero', true)}
            ></ha-switch>
          </ha-formfield>
        </div>
      </div>
    `;
  }

  _valueChanged(ev, field, isBoolean = false) {
    const value = isBoolean ? ev.target.checked : ev.detail.value;
    const newConfig = { ...this._config, [field]: value };
    
    const event = new CustomEvent("config-changed", {
      detail: { config: newConfig },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }
}

customElements.define("long-form-countdown-card", LongFormCountdownCard);
customElements.define("long-form-countdown-editor", LongFormCountdownEditor);

// --- DASHBOARD REGISTRATION ---
window.customCards = window.customCards || [];
window.customCards.push({
  type: "long-form-countdown-card",
  name: "Long Form Word Countdown Card",
  description: "A custom card for the Long Form Word Countdown integration.",
  preview: true,
});
