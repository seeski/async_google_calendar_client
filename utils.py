from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


def to_rfc3339(dt: datetime) -> str:
    """Convert datetime to RFC3339 string format."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=3)))
    dt = dt.replace(microsecond=0)
    s = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]


def build_event_body(
    start_dt: datetime,
    end_dt: Optional[datetime] = None,
    summary: str = "Session",
    description: str = "",
    location: str = "",
    attendees: Optional[List[Dict[str, Any]]] = None,
    timezone_str: str = "Europe/Moscow",
    recurrence: Optional[List[str]] = None,
    reminders: Optional[Dict[str, Any]] = None,
    **extra_fields,
) -> Dict[str, Any]:
    """Build event payload for Google Calendar API."""
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone(timedelta(hours=3)))
    if end_dt is None:
        end_dt = start_dt + timedelta(minutes=50)

    event: Dict[str, Any] = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": to_rfc3339(start_dt), "timeZone": timezone_str},
        "end": {"dateTime": to_rfc3339(end_dt), "timeZone": timezone_str},
    }

    if attendees:
        event["attendees"] = attendees
    if recurrence:
        event["recurrence"] = recurrence
    if reminders:
        event["reminders"] = reminders
    if extra_fields:
        event.update(extra_fields)
    return event
