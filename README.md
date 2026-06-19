# MaintainX HACS Integration

A minimal Home Assistant custom integration for MaintainX that allows you to create work orders from automations and includes Lovelace custom cards.

## Features

- **Integration setup** via config flow — store your MaintainX API key securely.
- **Service**: `maintainx.create_work_order` — call from automations to create work orders.
- **Lovelace custom cards**:
  - `maintainx-workorder-card` — UI form to create a work order manually.
  - `maintainx-list-card` — placeholder card for recent work orders.

## Installation via HACS

1. In HACS → **Integrations** → **+** button → **Add custom repository**
   - Repository URL: `https://github.com/homeassistantserverbrownsea-ux/MaintainX-Hacs`
   - Category: **Integration** (and **Frontend** if you want HACS to manage the Lovelace cards)
2. **Install** the repository from HACS.
3. **Restart** Home Assistant.
4. Go to **Settings** → **Devices & Services** → **Add Integration** → search for **MaintainX**.
5. Enter your MaintainX API key when prompted.

## Usage

### Service Call

After setup, the service `maintainx.create_work_order` is available.

**Example automation**:
```yaml
alias: Create MaintainX work order on leak
trigger:
  - platform: state
    entity_id: binary_sensor.basement_leak
    to: "on"
action:
  - service: maintainx.create_work_order
    data:
      title: "Basement leak detected"
      description: "Leak sensor triggered at {{ now().isoformat() }}. Check sump pump."
      priority: "high"
      location_id: "1234"
      assignee_id: "5678"
```

### Lovelace Cards

Add the Lovelace resources (HACS may add these automatically):
- `/hacsfiles/maintainx/maintainx-workorder-card.js`
- `/hacsfiles/maintainx/maintainx-list-card.js`

**Example dashboard YAML**:
```yaml
- type: custom:maintainx-workorder-card
  title: "Create Work Order"
  summary: "Example issue"
  description: "Describe the maintenance issue"

- type: custom:maintainx-list-card
  title: "Recent Work Orders"
```

## API Configuration

The integration uses `https://api.maintainx.com/v1` as the default API base URL. If you need a different endpoint, edit `custom_components/maintainx/api.py` and update the `BASE_URL` variable.

## Notes

- The API key is stored securely in Home Assistant's config entries (not in plaintext config files).
- Work order payload fields (title, description, priority, assignee_id, location_id, etc.) must match your MaintainX API schema. Adjust the payload in automations as needed.
- The list card is a placeholder; implement backend fetching (via `get_recent_work_orders()` in `api.py`) to populate it with recent orders.

## Contributing

Feel free to submit issues or PRs for improvements, bug fixes, or additional features (e.g., DataUpdateCoordinator, entities, options flow).
