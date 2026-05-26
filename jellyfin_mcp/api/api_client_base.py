# Generated base client
from typing import Any
from urllib.parse import urljoin

import requests


class ApiBase:
    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        verify: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self.username = username
        self.password = password
        self._session = requests.Session()
        self._session.verify = verify
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
