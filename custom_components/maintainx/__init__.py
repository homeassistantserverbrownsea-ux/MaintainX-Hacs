"""MaintainX integration - config entry, service registration, and frontend setup."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol

from .const import DOMAIN, CONF_API_KEY, SERVICE_CREATE_WORK_ORDER
from .api import MaintainXClient

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONF_API_KEY): str,
        })
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MaintainX integration from YAML config."""
    hass.data.setdefault(DOMAIN, {})
    
    if DOMAIN not in config:
        return True
    
    conf = config[DOMAIN]
    api_key = conf.get(CONF_API_KEY)
    
    if not api_key:
        _LOGGER.error("MaintainX: api_key is required in configuration.yaml")
        return False
    
    try:
        client = MaintainXClient(api_key)
        hass.data[DOMAIN]["client"] = client
        
        async def async_create_work_order(call: ServiceCall) -> None:
            """Service handler to create a work order in MaintainX."""
            payload: dict[str, Any] = call.data or {}
            try:
                result = await client.create_work_order(payload)
                _LOGGER.info("MaintainX created work order: %s", result)
                hass.bus.async_fire(f"{DOMAIN}_work_order_created", {"result": result})
            except Exception as err:
                _LOGGER.exception("Failed creating MaintainX work order: %s", err)

        hass.services.async_register(DOMAIN, SERVICE_CREATE_WORK_ORDER, async_create_work_order)
        _LOGGER.info("MaintainX integration set up from YAML config")
        return True
    except Exception as err:
        _LOGGER.error("MaintainX setup failed: %s", err)
        return False


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up an entry created via config flow."""
    try:
        api_key = entry.data.get(CONF_API_KEY)
        if not api_key:
            _LOGGER.error("MaintainX: Missing API key in config entry")
            return False
        
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
                hass.bus.async_fire(f"{DOMAIN}_work_order_created", {"result": result})
            except Exception as err:
                _LOGGER.exception("Failed creating MaintainX work order: %s", err)

        hass.services.async_register(DOMAIN, SERVICE_CREATE_WORK_ORDER, async_create_work_order)
        _LOGGER.info("MaintainX integration set up from config entry")
        return True
    except Exception as err:
        _LOGGER.error("MaintainX setup_entry failed: %s", err)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and clean up."""
    try:
        data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if data and "client" in data:
            try:
                await data["client"].async_close()
            except Exception:
                _LOGGER.exception("Error closing MaintainX client")

        if not hass.data.get(DOMAIN):
            hass.services.async_remove(DOMAIN, SERVICE_CREATE_WORK_ORDER)
        
        return True
    except Exception as err:
        _LOGGER.error("MaintainX unload failed: %s", err)
        return False
