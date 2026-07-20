# Generated base client
from typing import Any
from urllib.parse import urljoin

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class ApiBase:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = base_url
        self.token = token
        self.username = username
        self.password = password
        self.tls_profile = tls_profile or resolve_configured_tls_profile("jellyfin")
        self._session = self.tls_profile.configure_requests_session(requests.Session())
        if token:
            self._session.headers.update({"X-Emby-Token": token})

        from agent_utilities.core.exceptions import AuthError, UnauthorizedError

        try:
            response = self._session.get(urljoin(self.base_url, "/System/Info"))
            if response.status_code == 401:
                raise AuthError(
                    "Jellyfin authentication failed: Invalid token or credentials."
                )
            elif response.status_code == 403:
                raise UnauthorizedError(
                    "Jellyfin access forbidden: Insufficient permissions."
                )
            response.raise_for_status()
        except Exception as e:
            if isinstance(e, (AuthError, UnauthorizedError)):
                raise e

            pass

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self._session.close()
        self.tls_profile.cleanup()

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        json_data: dict | None = None,
    ) -> Any:
        url = urljoin(self.base_url, endpoint)
        response = self._session.request(
            method, url, params=params, data=data, json=json_data
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text
