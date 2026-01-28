class LongFormCountdownCard extends HTMLElement {
  // 1. Mandatory for custom elements
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  // 2. Set the configuration from the Dashboard YAML
  setConfig(config) {
    if (!config.entity) {
      throw new Error("You need to define an entity");
    }
    this.config = config;
  }

  // 3. This runs whenever the sensor updates
  set hass(hass) {
    const entityId = this.config.entity;
    const stateObj = hass.states[entityId];

    if (!stateObj) {
      this.shadowRoot.innerHTML = `
        <ha-card style="padding: 16px; color: red;">
          Entity not found: ${entityId}
        </ha-card>`;
      return;
    }

    const state = stateObj.state;
    const name = this.config.name || stateObj.attributes.friendly_name || entityId;

    this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          padding: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .name {
          font-size: 14px;
          color: var(--secondary-text-color);
          margin-bottom: 8px;
        }
        .state {
          font-size: 1.5rem;
          font-weight: bold;
          color: var(--primary-color);
        }
      </style>
      <ha-card>
        <div class="name">${name}</div>
        <div class="state">${state}</div>
      </ha-card>
    `;
  }
}

// Register the card name
customElements.define("long-form-countdown-card", LongFormCountdownCard);

// Add to the card picker list (even without an editor, it will show up)
window.customCards = window.customCards || [];
window.customCards.push({
  type: "long-form-countdown-card",
  name: "Long Form Countdown Card",
  description: "A simple card to display long-form countdown sensors."
});
