from datetime import datetime
from typing import Any, Dict, List, Optional
from gcalendar_client.http_client import HTTPClient
from gcalendar_client.utils import to_rfc3339


class FreeBusyService:
    """Service to check free/busy information for calendars."""

    def __init__(self, http_client: HTTPClient, default_calendar_id: Optional[str] = None):
        self.http_client = http_client
        self.default_calendar_id = default_calendar_id
        self.BASE_URL = "https://www.googleapis.com/calendar/v3"

    def _resolve_calendar_id(self, calendar_id: Optional[str]) -> str:
        cid = calendar_id or self.default_calendar_id
        if cid is None:
            raise ValueError(
                "calendar_id must be provided either in method or at client initialization."
            )
        return cid

    async def query_freebusy(
        self,
        start_dt: datetime,
        end_dt: datetime,
        calendar_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Query busy times for a given calendar within a datetime range.

        :param start_dt: Start datetime
        :param end_dt: End datetime
        :param calendar_id: Optional calendar ID
        """
        cid = self._resolve_calendar_id(calendar_id)
        url = f"{self.BASE_URL}/freeBusy"
        body = {
            "timeMin": to_rfc3339(start_dt),
            "timeMax": to_rfc3339(end_dt),
            "timeZone": "Europe/Moscow",
            "items": [{"id": cid}],
        }
        return (await self.http_client.post(url, body)).get("calendars", {}).get(cid, {}).get("busy", [])

    async def fetch_busy_slots_for_day(
        self,
        start_dt: datetime,
        end_dt: datetime,
        calendar_id: Optional[str] = None,
    ) -> list[str]:
        """
        Returns busy time slots (HH:MM) for the given day.

        :param start_dt: Start datetime
        :param end_dt: End datetime
        :param calendar_id: Optional calendar ID
        """
        busy_periods = await self.query_freebusy(start_dt, end_dt, calendar_id)
        slots = set()
        for period in busy_periods:
            start = datetime.fromisoformat(period["start"])
            end = datetime.fromisoformat(period["end"])
            current = start.replace(minute=0, second=0, microsecond=0)
            while current < end:
                slot_end = current + timedelta(minutes=50)
                if not (end <= current or start >= slot_end):
                    slots.add(current.strftime("%H:%M"))
                current += timedelta(hours=1)
        return sorted(slots)
