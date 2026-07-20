"""Jellyfin client authentication and access token delegation.

CONCEPT:JF-OS.identity.access-delegation — Access Delegation
"""

import threading

import requests
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)
from fastmcp.utilities.logging import get_logger

local = threading.local()
from jellyfin_mcp.api_client import Api

logger = get_logger(name="JellyfinAuth")


def get_client(
    base_url=None,
    token=None,
    username=None,
    password=None,
    tls_profile: ResolvedTLSProfile | None = None,
) -> Api:
    """
    Single entry point for Jellyfin clients.

    CONCEPT:JF-OS.identity.access-delegation — Access Delegation
    """
    base_url = base_url if base_url is not None else setting("JELLYFIN_URL", None)
    token = token if token is not None else setting("JELLYFIN_API_KEY", None)
    username = username if username is not None else setting("JELLYFIN_USERNAME", None)
    password = password if password is not None else setting("JELLYFIN_PASSWORD", None)
    profile = tls_profile or resolve_configured_tls_profile("jellyfin")
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
            with requests.Session() as delegation_session:
                profile.configure_requests_session(delegation_session)
                resp = delegation_session.post(
                    token_endpoint,
                    data=exchange_data,
                    auth=(client_id, client_secret),
                    timeout=10,
                )
            resp.raise_for_status()
            jellyfin_token = resp.json()["access_token"]
        except Exception as e:
            logger.error("Delegation failed: error_type=%s", type(e).__name__)
            raise RuntimeError("Credential delegation failed") from e
        try:
            return Api(
                base_url=base_url,
                token=jellyfin_token,
                tls_profile=profile,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The delegated Jellyfin credentials are "
                "not valid. Please check the configured OIDC references and "
                "permissions."
            ) from e

    if token or (username and password):
        try:
            return Api(
                base_url=base_url,
                token=token,
                username=username,
                password=password,
                tls_profile=profile,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The configured Jellyfin credentials are not "
                "valid. Please check the configured credential and endpoint "
                "references."
            ) from e

    raise ValueError(
        "No auth method: Provide JELLYFIN_API_KEY, enable delegation, or set JELLYFIN_USERNAME/PASSWORD"
    )
