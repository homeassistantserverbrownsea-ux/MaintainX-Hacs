"""Minimal async MaintainX client using API key (aiohttp)."""
from __future__ import annotations
import aiohttp
import asyncio
import logging
from typing import Any, Dict, Optional

_LOGGER = logging.getLogger(__name__)

# Default base URL - adjust if MaintainX uses a different base
BASE_URL = "https://api.maintainx.com/v1"

class MaintainXClient:
    """Simple async client for MaintainX API."""

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        self._api_key = api_key
        self._base_url = base_url or BASE_URL
        self._session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        })

    async def async_close(self) -> None:
        """Close underlying HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def create_work_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a work order.

        The expected payload fields must match MaintainX API:
        - title (or summary)
        - description
        - priority
        - assignee_id
        - location_id
        Adjust endpoint path and payload to match the real API.
        """
        # Endpoint path may differ — change '/work_orders' if needed.
        url = f"{self._base_url}/work_orders"
        async with self._session.post(url, json=payload) as resp:
            text = await resp.text()
            if resp.status >= 400:
                _LOGGER.error("MaintainX API error %s: %s", resp.status, text)
                raise aiohttp.ClientResponseError(
                    request_info=resp.request_info,
                    history=resp.history,
                    status=resp.status,
                    message=text,
                )
            return await resp.json()

    async def get_work_orders(self, status: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Fetch work orders, optionally filtered by status."""
        url = f"{self._base_url}/work_orders"
        params = {"limit": limit}
        if status:
            params["status"] = status
        
        async with self._session.get(url, params=params) as resp:
            text = await resp.text()
            if resp.status >= 400:
                _LOGGER.error("MaintainX API error %s: %s", resp.status, text)
                raise aiohttp.ClientResponseError(
                    request_info=resp.request_info,
                    history=resp.history,
                    status=resp.status,
                    message=text,
                )
            return await resp.json()

    async def get_work_order_by_id(self, work_order_id: str) -> Dict[str, Any]:
        """Fetch a specific work order by ID."""
        url = f"{self._base_url}/work_orders/{work_order_id}"
        async with self._session.get(url) as resp:
            text = await resp.text()
            if resp.status >= 400:
                _LOGGER.error("MaintainX API error %s: %s", resp.status, text)
                raise aiohttp.ClientResponseError(
                    request_info=resp.request_info,
                    history=resp.history,
                    status=resp.status,
                    message=text,
                )
            return await resp.json()
