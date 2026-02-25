import os
import threading
import requests
from agent_utilities.base_utilities import to_boolean
from fastmcp.utilities.logging import get_logger
from jellyfin_mcp.jellyfin_api import Api

local = threading.local()
logger = get_logger(name="JellyfinAuth")

def get_client(
    base_url=os.getenv("JELLYFIN_URL", None),
    token=os.getenv("JELLYFIN_API_KEY", None),
    username=os.getenv("JELLYFIN_USERNAME", None),
    password=os.getenv("JELLYFIN_PASSWORD", None),
    verify: bool = to_boolean(string=os.getenv("JELLYFIN_SSL_VERIFY", "True")),
) -> Api:
    """
    Single entry point for Jellyfin clients.
    """
    config = {
        "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        "audience": os.environ.get("JELLYFIN_AUDIENCE", None),
        "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
        "token_endpoint": os.environ.get("OIDC_TOKEN_ENDPOINT", None),
        "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
        "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    }

    if not base_url:
        raise RuntimeError("JELLYFIN_URL not set")

    mcp_token = getattr(local, "user_token", None)

    if config.get("enable_delegation", False) and mcp_token:
        logger.info("Delegating MCP token to Jellyfin")
        exchange_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": mcp_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
            "audience": config["audience"],
            "scope": config["delegated_scopes"],
        }
        try:
            resp = requests.post(
                config["token_endpoint"],
                data=exchange_data,
                auth=(config["oidc_client_id"], config["oidc_client_secret"]),
                verify=verify,
            )
            resp.raise_for_status()
            jellyfin_token = resp.json()["access_token"]
            return Api(base_url=base_url, token=jellyfin_token, verify=verify)
        except Exception as e:
            logger.error(f"Delegation failed: {e}")
            raise

    if token or (username and password):
        return Api(
            base_url=base_url,
            token=token,
            username=username,
            password=password,
            verify=verify,
        )

    raise ValueError(
        "No auth method: Provide JELLYFIN_API_KEY, enable delegation, or set JELLYFIN_USERNAME/PASSWORD"
    )
