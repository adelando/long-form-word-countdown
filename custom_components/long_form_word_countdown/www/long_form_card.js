class LongFormCountdownCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    if (!config.entity) throw new Error("Please define an entity");
    this.config = {
      short_form: false,
      flash_zero: false,
      show_elapsed: true,
      timer_color: 'var(--primary-color)',
      font_size: '1.2',
      ...config
    };
  }

  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];

    if (!stateObj) {
      this.shadowRoot.innerHTML = `
        <ha-card style="padding:16px;color:var(--error-color);">
          Entity not found: ${entityId}
        </ha-card>`;
      return;
    }

    const isFinished = stateObj.attributes.finished || stateObj.attributes.total_seconds_left <= 0;
    let displayState = stateObj.state;

    // Zero-state logic
    if (isFinished) {
      if (this.config.flash_zero) {
        displayState = "Timer Complete";
      } else if (!this.config.show_elapsed) {
        displayState = "0 seconds";
      }
    }

    // Formatting logic
    if (this.config.short_form) {
      displayState = displayState
        .replace(/ years?/g, "y").replace(/ months?/g, "m").replace(/ days?/g, "d")
        .replace(/ hours?/g, "h").replace(/ minutes?/g, "m").replace(/ seconds?/g, "s");
    }

    this.shadowRoot.innerHTML = `
      <style>
        ha-card { padding: 16px; display: flex; align-items: center; background: var(--ha-card-background, var(--card-background-color, white)); border-radius: var(--ha-card-border-radius, 12px); box-shadow: var(--ha-card-box-shadow, none); border: var(--ha-card-border-width, 1px) solid var(--ha-card-border-color, var(--divider-color, #e0e0e0)); }
        .icon { margin-right: 16px; --mdc-icon-size: 40px; color: ${this.config.timer_color}; flex-shrink: 0; }
        .info { flex: 1; min-width: 0; }
        .name { font-size: 0.9rem; color: var(--secondary-text-color); margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .timer { font-size: ${this.config.font_size}rem; color: ${this.config.timer_color}; font-weight: 500; line-height: 1.2; }
        @keyframes blink { 50% { opacity: 0.3; } }
        .flashing { animation: blink 1s linear infinite; color: var(--error-color) !important; font-weight: bold; }
      </style>
      <ha-card>
        <ha-icon class="icon" icon="${stateObj.attributes.icon || 'mdi:timer-sand'}"></ha-icon>
        <div class="info">
          <div class="name">${stateObj.attributes.friendly_name || entityId}</div>
          <div class="timer ${(this.config.flash_zero && isFinished) ? 'flashing' : ''}">${displayState}</div>
        </div>
      </ha-card>
    `;
  }

  static getConfigElement() {
    return document.createElement("long-form-countdown-editor");
  }

  static getStubConfig() {
    return { entity: "", short_form: false, flash_zero: false, show_elapsed: true, timer_color: "var(--primary-color)", font_size: "1.2" };
  }
}

// --- VISUAL EDITOR COMPONENT ---
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
      <div style="display: flex; flex-direction: column; gap: 16px; padding: 10px;">
        <ha-entity-picker
          .hass=${this._hass}
          .value=${this._config.entity}
          .includeDomains=${['sensor']}
          .label="Select Countdown Sensor"
          @value-changed=${(ev) => this._valueChanged(ev, 'entity')}>
        </ha-entity-picker>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <ha-formfield label="Short Form">
            <ha-switch .checked=${this._config.short_form} @change=${(ev) => this._valueChanged(ev, 'short_form', true)}></ha-switch>
          </ha-formfield>
          <ha-formfield label="Flash on Finish">
            <ha-switch .checked=${this._config.flash_zero} @change=${(ev) => this._valueChanged(ev, 'flash_zero', true)}></ha-switch>
          </ha-formfield>
        </div>

        <div style="padding: 12px; background: var(--secondary-background-color); border-radius: 8px;">
          <div style="margin-bottom:10px;">
            <label>Font Size (rem)</label>
            <input type="number" step="0.1" value="${this._config.font_size}" @change=${(ev) => this._valueChanged(ev, 'font_size')} style="width: 100%; height: 32px;">
          </div>
          <div>
            <label>Timer Color</label>
            <input type="text" value="${this._config.timer_color}" @change=${(ev) => this._valueChanged(ev, 'timer_color')} style="width: 100%; height: 32px;">
          </div>
        </div>
      </div>
    `;
  }

  _valueChanged(ev, field, isBool = false) {
    const newValue = isBool ? ev.target.checked : (ev.detail?.value || ev.target.value);
    const config = { ...this._config, [field]: newValue };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config },
      bubbles: true,
      composed: true
    }));
  }
}

customElements.define("long-form-countdown-card", LongFormCountdownCard);
customElements.define("long-form-countdown-editor", LongFormCountdownEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "long-form-countdown-card",
  name: "Long Form Word Countdown",
  description: "Advanced countdown with styling options.",
  preview: true
});
