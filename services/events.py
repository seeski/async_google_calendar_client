from datetime import datetime
from typing import Any, Dict, List, Optional
from http import HTTPClient
from utils import to_rfc3339


class EventService:
    """Service for managing Google Calendar events."""

    def __init__(self, http_client: HTTPClient, default_calendar_id: Optional[str] = None):
        self.http_client = http_client
        self.default_calendar_id = default_calendar_id
        self.BASE_URL = "https://www.googleapis.com/calendar/v3"

    def _resolve_calendar_id(self, calendar_id: Optional[str]) -> str:
        cid = calendar_id or self.default_calendar_id
        if cid is None:
            raise ValueError("calendar_id must be provided either in method or at client initialization.")
        return cid

    async def create_event(self, event: Dict[str, Any], calendar_id: Optional[str] = None) -> Dict[str, Any]:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events"
        return await self.http_client.post(url, event)

    async def get_event(self, event_id: str, calendar_id: Optional[str] = None) -> Dict[str, Any]:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events/{event_id}"
        return await self.http_client.get(url)

    async def update_event(self, event_id: str, event_data: Dict[str, Any], calendar_id: Optional[str] = None) -> Dict[str, Any]:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events/{event_id}"
        return await self.http_client.post(url, event_data)

    async def patch_event(self, event_id: str, event_data: Dict[str, Any], calendar_id: Optional[str] = None) -> Dict[str, Any]:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events/{event_id}"
        return await self.http_client.patch(url, event_data)

    async def delete_event(self, event_id: str, calendar_id: Optional[str] = None) -> bool:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events/{event_id}"
        return await self.http_client.delete(url)

    async def list_events(self, start_dt: datetime, end_dt: datetime, calendar_id: Optional[str] = None) -> List[Dict[str, Any]]:
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/calendars/{cid}/events"
        params = {
            "timeMin": to_rfc3339(start_dt),
            "timeMax": to_rfc3339(end_dt),
            "singleEvents": True,
            "orderBy": "startTime",
        }
        return await self.http_client.get(url, params)
