from typing import Any, Dict, List, Optional, Coroutine
from http import HTTPClient


class CalendarService:
    """Service to manage calendars."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.BASE_URL = "https://www.googleapis.com/calendar/v3"

    async def list_calendars(self) -> dict[str, Any]:
        """List all calendars available to the service account."""
        url = f"{self.BASE_URL}/users/me/calendarList"
        return await self.http_client.get(url)

    async def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """Retrieve a calendar by its ID."""
        url = f"{self.BASE_URL}/calendars/{calendar_id}"
        return await self.http_client.get(url)

    async def create_calendar(self, summary: str, time_zone: str = "Europe/Moscow") -> Dict[str, Any]:
        """Create a new calendar."""
        url = f"{self.BASE_URL}/calendars"
        data = {"summary": summary, "timeZone": time_zone}
        return await self.http_client.post(url, data)

    async def update_calendar(self, calendar_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing calendar."""
        url = f"{self.BASE_URL}/calendars/{calendar_id}"
        return await self.http_client.patch(url, data)

    async def delete_calendar(self, calendar_id: str) -> bool:
        """Delete a calendar by its ID."""
        url = f"{self.BASE_URL}/calendars/{calendar_id}"
        return await self.http_client.delete(url)
