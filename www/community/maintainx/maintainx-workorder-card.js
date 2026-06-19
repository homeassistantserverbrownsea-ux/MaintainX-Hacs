class MaintainXWorkorderCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  setConfig(config) {
    this._config = config || {};
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  _render() {
    if (!this._hass) return;
    const title = this._config.title || 'Create Work Order';
    const defaultSummary = this._config.summary || '';
    const defaultDescription = this._config.description || '';

    this.shadowRoot.innerHTML = `
      <style>
        .card { padding: 12px; background: var(--card-background-color); color: var(--primary-text-color); border-radius: 8px; font-family: Roboto, Arial; }
        input, textarea { width: 100%; box-sizing: border-box; margin-top: 6px; }
        button { margin-top: 8px; padding: 6px 10px; }
        #result { margin-top:8px; font-size: 0.9em; color: var(--secondary-text-color); }
      </style>
      <div class="card">
        <h3>${title}</h3>
        <div>
          <label>Title<input id="title" .value="${defaultSummary}" placeholder="Title"></label>
        </div>
        <div>
          <label>Description<textarea id="description" placeholder="Description">${defaultDescription}</textarea></label>
        </div>
        <div>
          <label>Priority
            <select id="priority">
              <option value="">(default)</option>
              <option value="low">low</option>
              <option value="medium">medium</option>
              <option value="high">high</option>
            </select>
          </label>
        </div>
        <button id="create">Create Work Order</button>
        <div id="result"></div>
      </div>
    `;

    this.shadowRoot.querySelector('#create').addEventListener('click', () => {
      const payload = {
        title: this.shadowRoot.querySelector('#title').value,
        description: this.shadowRoot.querySelector('#description').value,
        priority: this.shadowRoot.querySelector('#priority').value || undefined,
      };
      this._hass.callService('maintainx', 'create_work_order', payload);
      this.shadowRoot.querySelector('#result').textContent = 'Requested creation...';
    });
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('maintainx-workorder-card', MaintainXWorkorderCard);
