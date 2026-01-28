// Check if the element is already defined to prevent errors on refresh
if (!customElements.get("long-form-countdown-card")) {
  class LongFormCountdownCard extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
    }

    setConfig(config) {
      if (!config.entity) throw new Error("Please define an entity");
      this.config = config;
    }

    set hass(hass) {
      const entityId = this.config.entity;
      const stateObj = hass.states[entityId];

      if (!stateObj) {
        this.shadowRoot.innerHTML = `<ha-card style="padding:16px;color:red;">Entity Not Found</ha-card>`;
        return;
      }

      this.shadowRoot.innerHTML = `
        <ha-card style="padding: 16px;">
          <div style="font-size: 14px; color: var(--secondary-text-color);">${stateObj.attributes.friendly_name || entityId}</div>
          <div style="font-size: 1.2rem; font-weight: bold;">${stateObj.state}</div>
        </ha-card>
      `;
    }
  }

  customElements.define("long-form-countdown-card", LongFormCountdownCard);
}

// Ensure the card appears in the UI picker
window.customCards = window.customCards || [];
const cardExists = window.customCards.some(c => c.type === "long-form-countdown-card");
if (!cardExists) {
  window.customCards.push({
    type: "long-form-countdown-card",
    name: "Long Form Countdown",
    description: "Display your long-form sensor",
    preview: true
  });
}
