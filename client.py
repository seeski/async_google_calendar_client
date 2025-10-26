from typing import Optional
from http import HTTPClient
from services import (
    EventService,
    CalendarService,
    FreeBusyService
)


class AsyncGCalendarClient:
    """
    Main client for Google Calendar API.

    :param service_account_file: Path to service account JSON
    :param calendar_id: Optional default calendar ID
    """

    def __init__(self, service_account_file: str, calendar_id: Optional[str] = None):
        self.http_client = HTTPClient(service_account_file)
        self.default_calendar_id = calendar_id
        self.events = EventService(self.http_client, calendar_id)
        self.calendars = CalendarService(self.http_client)
        self.free_busy = FreeBusyService(self.http_client, calendar_id)

    async def __aenter__(self) -> "AsyncGCalendarClient":
        await self.http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.http_client.__aexit__(exc_type, exc_val, exc_tb)
