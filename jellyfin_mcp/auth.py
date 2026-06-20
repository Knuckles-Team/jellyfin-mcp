"""Jellyfin client authentication and access token delegation.

CONCEPT:JELLYFIN-4.0 — Access Delegation
"""

import threading

import requests
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from fastmcp.utilities.logging import get_logger

local = threading.local()
from jellyfin_mcp.api_client import Api

logger = get_logger(name="JellyfinAuth")


def get_client(
    base_url=None,
    token=None,
    username=None,
    password=None,
    verify: bool | None = None,
) -> Api:
    """
    Single entry point for Jellyfin clients.

    CONCEPT:JELLYFIN-4.0 — Access Delegation
    """
    base_url = base_url if base_url is not None else setting("JELLYFIN_URL", None)
    token = token if token is not None else setting("JELLYFIN_API_KEY", None)
    username = username if username is not None else setting("JELLYFIN_USERNAME", None)
    password = password if password is not None else setting("JELLYFIN_PASSWORD", None)
    verify = verify if verify is not None else setting("JELLYFIN_SSL_VERIFY", True)
    config = {
        "enable_delegation": setting("ENABLE_DELEGATION", False),
        "audience": setting("JELLYFIN_AUDIENCE", None),
        "delegated_scopes": setting("DELEGATED_SCOPES", "api"),
        "token_endpoint": setting("OIDC_TOKEN_ENDPOINT", None),
        "oidc_client_id": setting("OIDC_CLIENT_ID", None),
        "oidc_client_secret": setting("OIDC_CLIENT_SECRET", None),
    }

    if not base_url:
        raise RuntimeError("JELLYFIN_URL not set")

    mcp_token = getattr(local, "user_token", None)

    if config.get("enable_delegation", False) and mcp_token:
        logger.info("Delegating MCP token to Jellyfin")
        token_endpoint = config.get("token_endpoint")
        client_id = config.get("oidc_client_id")
        client_secret = config.get("oidc_client_secret")
        if (
            not isinstance(token_endpoint, str)
            or not isinstance(client_id, str)
            or not isinstance(client_secret, str)
        ):
            raise RuntimeError(
                "OIDC delegation configuration is incomplete. Must specify OIDC_TOKEN_ENDPOINT, OIDC_CLIENT_ID, and OIDC_CLIENT_SECRET."
            )

        exchange_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": mcp_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",  # nosec B105
            "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",  # nosec B105
            "audience": config["audience"],
            "scope": config["delegated_scopes"],
        }
        try:
            resp = requests.post(
                token_endpoint,
                data=exchange_data,
                auth=(client_id, client_secret),
                verify=verify,
                timeout=10,
            )
            resp.raise_for_status()
            jellyfin_token = resp.json()["access_token"]
            try:
                return Api(base_url=base_url, token=jellyfin_token, verify=verify)
            except (AuthError, UnauthorizedError) as e:
                raise RuntimeError(
                    f"AUTHENTICATION ERROR: The delegated Jellyfin credentials are not valid for '{base_url}'. "
                    f"Please check your OIDC configuration and permissions. "
                    f"Error details: {str(e)}"
                ) from e
        except Exception as e:
            logger.error(f"Delegation failed: {e}")
            raise

    if token or (username and password):
        try:
            return Api(
                base_url=base_url,
                token=token,
                username=username,
                password=password,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The Jellyfin credentials provided are not valid for '{base_url}'. "
                f"Please check your JELLYFIN_API_KEY (or JELLYFIN_USERNAME/JELLYFIN_PASSWORD) and JELLYFIN_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    raise ValueError(
        "No auth method: Provide JELLYFIN_API_KEY, enable delegation, or set JELLYFIN_USERNAME/PASSWORD"
    )
