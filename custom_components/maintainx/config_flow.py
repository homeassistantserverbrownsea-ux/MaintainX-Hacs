"""Config flow for MaintainX integration (API key)."""
from __future__ import annotations

import voluptuous as vol
import logging

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

class MaintainXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MaintainX."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step - User initiated config."""
        errors = {}
        
        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY, "").strip()
            
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                await self.async_set_unique_id("maintainx")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title="MaintainX",
                    data={CONF_API_KEY: api_key}
                )

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY, description={"suggested_value": ""}): str,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this config entry."""
        return MaintainXOptionsFlowHandler(config_entry)


class MaintainXOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for MaintainX."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        return self.async_show_form(step_id="init")
