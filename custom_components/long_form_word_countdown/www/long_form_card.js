class LongFormCountdownCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) throw new Error("Please define an entity");
    this.config = config;
  }

  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];

    if (!stateObj) {
      this.innerHTML = `<ha-card style="padding:16px;color:red;">Entity not found: ${entityId}</ha-card>`;
      return;
    }

    const isFinished = stateObj.attributes.finished || stateObj.attributes.total_seconds_left <= 0;
    let displayState = stateObj.state;

    if (isFinished && this.config.flash_zero) {
        displayState = "Timer Complete";
    }

    this.innerHTML = `
      <ha-card style="padding: 16px;">
        <div style="display: flex; align-items: center;">
          <ha-icon icon="${stateObj.attributes.icon || 'mdi:timer-sand'}" style="margin-right: 16px; color: var(--primary-color);"></ha-icon>
          <div>
            <div style="font-size: 0.9rem; color: var(--secondary-text-color);">${stateObj.attributes.friendly_name}</div>
            <div style="font-size: 1.1rem;">${displayState}</div>
          </div>
        </div>
      </ha-card>
    `;
  }

  // This links the card to the editor below
  static getConfigElement() {
    return document.createElement("long-form-countdown-editor");
  }

  static getStubConfig() {
    return { entity: "", flash_zero: false, short_form: false };
  }
}

// Visual Editor Class
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
      <div style="padding: 10px;">
        <ha-entity-picker
          .hass=${this._hass}
          .value=${this._config.entity}
          .includeDomains=${['sensor']}
          .label="Select Countdown Sensor"
          @value-changed=${this._entityChanged.bind(this)}>
        </ha-entity-picker>
      </div>
    `;
  }

  _entityChanged(ev) {
    if (!this._config || !ev.detail.value) return;
    const newConfig = { ...this._config, entity: ev.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: newConfig },
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
  description: "Display your word-based countdowns.",
  preview: true
});
