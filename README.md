# 🚀 Async Google Calendar Client

Асинхронный Python-клиент для работы с [Google Calendar API](https://developers.google.com/calendar).  
Позволяет управлять календарями, событиями и проверять занятость (free/busy) с использованием сервисного аккаунта.

✨ **Особенности:**
- Полностью асинхронная работа через `async/await`
- Управление календарями и событиями
- Проверка занятости (Free/Busy)
___
## 🛠 Возможности

- 📅 Управление календарями:
  - Список календарей
  - Создание, обновление и удаление календарей
- 🎫 Управление событиями:
  - Создание, получение, обновление и удаление событий
  - Получение списка событий за период времени
- ⏰ Проверка занятости (Free/Busy):
  - Получение занятых временных слотов
___
## ⚡ Установка

Установите зависимости:

```bash
   pip install httpx google-auth
```

>  Рекомендуется использовать виртуальное окружение 🐍
___
## 🔧 Настройка

1. Создайте сервисный аккаунт в [Google Cloud Console](https://console.cloud.google.com/)  
2. Скачайте JSON-файл с ключами сервисного аккаунта  
3. Дайте сервисному аккаунту доступ к нужным календарям
 ___
## 🏃‍♂️ Использование

Пример использования:

```python
import asyncio
from async_google_calendar_client import AsyncGCalendarClient
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = "path/to/service_account.json"
CALENDAR_ID = "your_calendar_id@example.com"

async def main():
    async with AsyncGCalendarClient(SERVICE_ACCOUNT_FILE, CALENDAR_ID) as client:
        # Получить список календарей
        calendars = await client.calendars.list_calendars()
        print(calendars)

        # Создать событие
        start_dt = datetime.utcnow()
        end_dt = start_dt + timedelta(hours=1)
        event_body = {
            "summary": "Тестовое событие",
            "start": {"dateTime": start_dt.isoformat(), "timeZone": "Europe/Moscow"},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": "Europe/Moscow"},
        }
        event = await client.events.create_event(event_body)
        print(event)

        # Проверка занятости
        busy_slots = await client.free_busy.fetch_busy_slots_for_day(start_dt, end_dt)
        print("Занятые слоты:", busy_slots)

asyncio.run(main())
```

---

## 📚 API

### AsyncGCalendarClient
- `events` — объект `EventService` для работы с событиями  
- `calendars` — объект `CalendarService` для работы с календарями  
- `free_busy` — объект `FreeBusyService` для проверки занятости

### 🎫 EventService

- `create_event(event: dict, calendar_id: Optional[str])`  
- `get_event(event_id: str, calendar_id: Optional[str])`  
- `update_event(event_id: str, event_data: dict, calendar_id: Optional[str])`  
- `patch_event(event_id: str, event_data: dict, calendar_id: Optional[str])`  
- `delete_event(event_id: str, calendar_id: Optional[str])`  
- `list_events(start_dt: datetime, end_dt: datetime, calendar_id: Optional[str])`

### 📅 CalendarService

- `list_calendars()`  
- `get_calendar(calendar_id: str)`  
- `create_calendar(summary: str, time_zone: str = "Europe/Moscow")`  
- `update_calendar(calendar_id: str, data: dict)`  
- `delete_calendar(calendar_id: str)`

### ⏰ FreeBusyService

- `query_freebusy(start_dt: datetime, end_dt: datetime, calendar_id: Optional[str])`  
- `fetch_busy_slots_for_day(start_dt: datetime, end_dt: datetime, calendar_id: Optional[str])`

## 🛠 Вспомогательные функции

- `to_rfc3339(dt: datetime) -> str` — конвертирует datetime в формат RFC3339  
- `build_event_body(...) -> dict` — формирует тело события для Google Calendar API

