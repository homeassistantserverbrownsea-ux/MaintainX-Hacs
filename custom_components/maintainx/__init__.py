"""MaintainX integration - basic config entry, service registration and client lifecycle."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_API_KEY, SERVICE_CREATE_WORK_ORDER
from .api import MaintainXClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MaintainX integration (only used for legacy YAML if needed)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up an entry created via config flow."""
    api_key = entry.data.get(CONF_API_KEY)
    client = MaintainXClient(api_key)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "entry": entry,
    }

    async def async_create_work_order(call: ServiceCall) -> None:
        """Service handler to create a work order in MaintainX."""
        payload: dict[str, Any] = call.data or {}
        try:
            result = await client.create_work_order(payload)
            _LOGGER.info("MaintainX created work order: %s", result)
            # Fire event so automations/Frontend can react to created work orders
            hass.bus.async_fire(f"{DOMAIN}_work_order_created", {"result": result})
        except Exception as err:
            _LOGGER.exception("Failed creating MaintainX work order: %s", err)
            # Re-raise or just log depending on desired behavior
            raise

    hass.services.async_register(DOMAIN, SERVICE_CREATE_WORK_ORDER, async_create_work_order)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and clean up."""
    data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if data and "client" in data:
        try:
            await data["client"].async_close()
        except Exception:  # avoid unload failure due to close
            _LOGGER.exception("Error closing MaintainX client")

    # Remove service if no other entries remain
    if not hass.data.get(DOMAIN):
        hass.services.async_remove(DOMAIN, SERVICE_CREATE_WORK_ORDER)

    return True
