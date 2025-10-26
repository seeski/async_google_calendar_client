import json
from typing import Any, Dict, Optional
import httpx
from google.oauth2 import service_account
from google.auth.transport.requests import Request


class HTTPClient:
    """Asynchronous HTTP client for Google API."""

    def __init__(self, service_account_file: str):
        self._client: Optional[httpx.AsyncClient] = None
        self._creds: Optional[service_account.Credentials] = None
        self._service_account_file = service_account_file
        self._init_creds()

    def _init_creds(self) -> None:
        """Initialize service account credentials."""
        self._creds = service_account.Credentials.from_service_account_file(
            self._service_account_file,
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

    def _ensure_token(self) -> None:
        """Refresh the token if invalid."""
        if not self._creds.valid or self._creds.token is None:
            self._creds.refresh(Request())

    async def __aenter__(self) -> "HTTPClient":
        self._client = httpx.AsyncClient(timeout=20)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _build_headers(self, content_type: Optional[str] = None) -> Dict[str, str]:
        self._ensure_token()
        headers: Dict[str, str] = {"Authorization": f"Bearer {self._creds.token}"}
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        headers = self._build_headers()
        try:
            resp = await self._client.get(url, headers=headers, params=params or {})
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            return {"error": f"{type(e).__name__}: {e}"}

    async def post(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        headers = self._build_headers("application/json")
        try:
            resp = await self._client.post(url, headers=headers, content=json.dumps(data))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            return {"error": f"{type(e).__name__}: {e}"}

    async def patch(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        headers = self._build_headers("application/json")
        try:
            resp = await self._client.patch(url, headers=headers, content=json.dumps(data))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            return {"error": f"{type(e).__name__}: {e}"}

    async def delete(self, url: str) -> bool:
        headers = self._build_headers()
        try:
            resp = await self._client.delete(url, headers=headers)
            resp.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
