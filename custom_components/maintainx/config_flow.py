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
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY, "").strip()
            
            # Basic validation
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                # Create entry with the API key
                await self.async_set_unique_id("maintainx")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title="MaintainX",
                    data={CONF_API_KEY: api_key}
                )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "docs_url": "https://github.com/homeassistantserverbrownsea-ux/MaintainX-Hacs"
            }
        )
