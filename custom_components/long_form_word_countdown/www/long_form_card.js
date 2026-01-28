class LongFormCountdownCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("Please define an entity");
    }
    // Set defaults immediately to avoid 'undefined' errors
    this.config = {
      short_form: false,
      flash_zero: false,
      show_elapsed: true,
      timer_color: 'var(--primary-color)',
      font_size: '1.1',
      ...config
    };
  }

  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];

    if (!stateObj) {
      this.shadowRoot.innerHTML = `
        <ha-card style="padding: 16px; color: red;">
          Entity not found: ${entityId}
        </ha-card>
      `;
      return;
    }

    const isFinished = stateObj.attributes.finished || stateObj.attributes.total_seconds_left <= 0;
    let displayState = stateObj.state;

    // Logic for Flash vs Elapsed
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

    this.shadowRoot.innerHTML = `
      <ha-card style="padding: 16px;">
        <div style="display: flex; align-items: center;">
          <ha-icon icon="${stateObj.attributes.icon || 'mdi:timer-sand'}" 
            style="margin-right: 16px; --mdc-icon-size: 40px; color: ${this.config.timer_color};">
          </ha-icon>
          <div style="flex: 1;">
            <div style="font-size: 0.9rem; color: var(--secondary-text-color); font-weight: 500;">
              ${stateObj.attributes.friendly_name || entityId}
            </div>
            <div id="timer" class="${(this.config.flash_zero && isFinished) ? 'flashing' : ''}" 
              style="line-height: 1.3; color: ${this.config.timer_color}; font-size: ${this.config.font_size}rem;">
              ${displayState}
            </div>
          </div>
        </div>
        <style>
          @keyframes blink { 50% { opacity: 0.3; } }
          .flashing { animation: blink 1s linear infinite; color: var(--error-color) !important; font-weight: bold; }
        </style>
      </ha-card>
    `;
  }

  static getConfigElement() {
    return document.createElement("long-form-countdown-editor");
  }

  static getStubConfig() {
    return { entity: "", short_form: false, flash_zero: false, show_elapsed: true };
  }
}

// --- EDITOR ---
class LongFormCountdownEditor extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (this._config) this._render();
  }
  setConfig(config) {
    this._config = config;
  }
  _render() {
    this.innerHTML = `
      <div style="padding: 20px;">
        <ha-entity-picker 
          .hass=${this._hass} 
          .value=${this._config.entity} 
          .includeDomains=${['sensor']}
          .label="Entity"
          @value-changed=${(ev) => this._valueChanged(ev, 'entity')}>
        </ha-entity-picker>
        <p>Use the Manual YAML editor to toggle other settings for now.</p>
      </div>
    `;
  }
  _valueChanged(ev, field) {
    const newConfig = { ...this._config, [field]: ev.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: newConfig }, bubbles: true, composed: true }));
  }
}

customElements.define("long-form-countdown-card", LongFormCountdownCard);
customElements.define("long-form-countdown-editor", LongFormCountdownEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "long-form-countdown-card",
  name: "Long Form Word Countdown",
  preview: true
});
