#!/usr/bin/env python3
import os
import logging
import argparse
from typing import Optional, Any
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import load_mcp_servers, MCPServerStreamableHTTP, MCPServerSSE
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from pydantic_ai.ui.ag_ui import AGUIAdapter
from pydantic_ai.ui import SSE_CONTENT_TYPE

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
import uvicorn

from jellyfin_mcp.utils import (
    to_integer,
    to_boolean,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    prune_large_messages,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = "0.1.1"

# Configuration
AGENT_NAME = "JellyfinAgent"
AGENT_DESCRIPTION = (
    "An intelligent agent for managing and interacting with a Jellyfin media server."
)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(os.getenv("PORT", "9001"))
DEFAULT_DEBUG = to_boolean(os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "gpt-4o")
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", None)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_SKILLS_DIRECTORY = os.getenv("SKILLS_DIRECTORY", get_skills_path())
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))

# Model Settings
DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "8192"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_SEED = to_integer(os.getenv("SEED", None))
DEFAULT_PRESENCE_PENALTY = to_float(os.getenv("PRESENCE_PENALTY", "0.0"))
DEFAULT_FREQUENCY_PENALTY = to_float(os.getenv("FREQUENCY_PENALTY", "0.0"))
DEFAULT_LOGIT_BIAS = to_dict(os.getenv("LOGIT_BIAS", None))
DEFAULT_STOP_SEQUENCES = to_list(os.getenv("STOP_SEQUENCES", None))
DEFAULT_EXTRA_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))
DEFAULT_EXTRA_BODY = to_dict(os.getenv("EXTRA_BODY", None))

# Prompts
SUPERVISOR_SYSTEM_PROMPT = """You are the Jellyfin Supervisor Agent.
Your goal is to assist the user by assigning tasks to specialized child agents through your available toolset.
Analyze the user's request and determine which domain(s) it falls into (Media, System, User, LiveTV, Devices).
Then, call the appropriate tool(s) to delegate the task.
Synthesize the results from the child agents into a final helpful response.
Always be warm, professional, and helpful.
"""

MEDIA_AGENT_PROMPT = """You are the Jellyfin Media Agent.
Your goal is to manage and retrieve media content.
This includes: Movies, TV Shows, Music, Artists, Albums, Genres, Playlists, Libraries, Items, Images, Traversing folders, and Streaming information.
Use your tools to find media, list items, get details, and manage library metadata.
"""

SYSTEM_AGENT_PROMPT = """You are the Jellyfin System Agent.
Your goal is to manage server system tasks.
This includes: Server Configuration, Activity Logs, Backend System info, Scheduled Tasks, Plugins, Packages, API Keys, Backups, and Localization.
Use your tools to check server status, logs, and configuration.
"""

USER_AGENT_PROMPT = """You are the Jellyfin User Agent.
Your goal is to manage user-centric interaction.
This includes: User accounts, User libraries, Views, Sessions, Playback Status (Playstate), Suggestions, Search, and Display Preferences.
Use your tools to manage users and their session data.
"""

LIVETV_AGENT_PROMPT = """You are the Jellyfin LiveTV Agent.
Your goal is to manage Live TV functionality.
This includes: Channels, Tuners, Guide info (if available via tags), and Recordings.
Use your tools to list channels and access live TV features.
"""

DEVICE_AGENT_PROMPT = """You are the Jellyfin Device Agent.
Your goal is to manage connected devices.
This includes: Listing devices, Device options, SyncPlay, QuickConnect, and Remote Image handling.
Use your tools to manage client devices connected to the server.
"""


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:

    logger.info("Initializing Jellyfin Agent System...")

    model = create_model(provider, model_id, base_url, api_key)
    settings = ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        top_p=DEFAULT_TOP_P,
        timeout=DEFAULT_TIMEOUT,
        parallel_tool_calls=DEFAULT_PARALLEL_TOOL_CALLS,
        seed=DEFAULT_SEED,
        presence_penalty=DEFAULT_PRESENCE_PENALTY,
        frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
        logit_bias=DEFAULT_LOGIT_BIAS,
        stop_sequences=DEFAULT_STOP_SEQUENCES,
        extra_headers=DEFAULT_EXTRA_HEADERS,
        extra_body=DEFAULT_EXTRA_BODY,
    )

    # Load master toolsets
    master_toolsets = []
    if mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        master_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")
    elif mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(mcp_url)
        else:
            server = MCPServerStreamableHTTP(mcp_url)
        master_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")

    # Load master toolsets
    master_toolsets = []
    if mcp_config and os.path.exists(mcp_config):
        try:
            # Assuming load_mcp_servers can handle the config file format
            # Note: Typically pydantic-ai's load_mcp_servers expects stdio config
            # If using SSE locally from the same package, we might need a direct server instance if not running separately
            # For now, assuming the config points to a running server or stdio command
            mcp_toolset = load_mcp_servers(mcp_config)
            master_toolsets.extend(mcp_toolset)
            logger.info(f"Connected to MCP Config: {mcp_config}")
        except Exception as e:
            logger.error(f"Failed to load MCP config: {e}")
    else:
        # Fallback: Try to run the default jellyfin_mcp tool if available in python path
        # Or warn user
        logger.warning(f"MCP Config file not found at {mcp_config}")

    if skills_directory and os.path.exists(skills_directory):
        master_toolsets.append(SkillsToolset(directories=[str(skills_directory)]))

    # Define Tag -> Agent Definitions
    # (prompt, name, tags)
    agent_defs = {
        "media": (
            MEDIA_AGENT_PROMPT,
            "Jellyfin_Media_Agent",
            [
                "Artists",
                "Audio",
                "Collection",
                "Genres",
                "HlsSegment",
                "Image",
                "ItemLookup",
                "ItemRefresh",
                "ItemUpdate",
                "Items",
                "Library",
                "LibraryStructure",
                "Lyrics",
                "MediaInfo",
                "MediaSegments",
                "Movies",
                "MusicGenres",
                "Persons",
                "Playlists",
                "RemoteImage",
                "Studios",
                "Subtitle",
                "Trailers",
                "TvShows",
                "UniversalAudio",
                "VideoAttachments",
                "Videos",
                "Years",
                "DynamicHls",
            ],
        ),
        "system": (
            SYSTEM_AGENT_PROMPT,
            "Jellyfin_System_Agent",
            [
                "ActivityLog",
                "ApiKey",
                "Backup",
                "Branding",
                "ClientLog",
                "Configuration",
                "Dashboard",
                "Environment",
                "Filter",
                "Localization",
                "Package",
                "Plugins",
                "ScheduledTasks",
                "Startup",
                "System",
                "TimeSync",
                "Tmdb",
            ],
        ),
        "user": (
            USER_AGENT_PROMPT,
            "Jellyfin_User_Agent",
            [
                "InstantMix",
                "Playstate",
                "QuickConnect",
                "Search",
                "Session",
                "Suggestions",
                "SyncPlay",
                "Trickplay",
                "User",
                "UserLibrary",
                "UserViews",
                "DisplayPreferences",
            ],
        ),
        "livetv": (
            LIVETV_AGENT_PROMPT,
            "Jellyfin_LiveTV_Agent",
            ["Channels", "LiveTv"],
        ),
        "device": (DEVICE_AGENT_PROMPT, "Jellyfin_Device_Agent", ["Devices"]),
    }

    child_agents = {}

    for tag_key, (system_prompt, agent_name, tags_list) in agent_defs.items():
        tag_toolsets = []
        for ts in master_toolsets:

            def filter_func(ctx, tool_def, t_list=tags_list):
                # Check if tool has Any of the tags in t_list
                # tool_def.tags is usually a list of strings
                if not tool_def.tags:
                    return False
                return any(t in tool_def.tags for t in t_list)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)

        agent = Agent(
            name=agent_name,
            system_prompt=system_prompt,
            model=model,
            model_settings=settings,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
        )
        child_agents[tag_key] = agent

    # Supervisor
    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        deps_type=Any,
    )

    @supervisor.tool
    async def assign_to_media_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a media-related task to the Media Agent (Content, Library, Items)."""
        return (
            await child_agents["media"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_to_system_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a system-related task to the System Agent (Config, Logs, System Info)."""
        return (
            await child_agents["system"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_to_user_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a user-related task to the User Agent (Users, Sessions, Playback)."""
        return (
            await child_agents["user"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_to_livetv_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a LiveTV-related task to the LiveTV Agent."""
        return (
            await child_agents["livetv"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_to_device_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a device-related task to the Device Agent."""
        return (
            await child_agents["device"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    return supervisor


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    debug: bool = DEFAULT_DEBUG,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
):
    print(
        f"Starting {AGENT_NAME} with provider={provider}, model={model_id}, mcp={mcp_url} | {mcp_config}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        skills_directory=skills_directory,
    )
    # Simple skills loading for default exposure in A2A
    skills = []
    if skills_directory and os.path.exists(skills_directory):
        skills = load_skills_from_directory(skills_directory)
    else:
        skills = [
            Skill(
                id="jellyfin",
                name="Jellyfin",
                description="Control Jellyfin Server",
                tags=["jellyfin"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=e.json(), media_type="application/json", status_code=422
            )

        if hasattr(run_input, "messages"):
            run_input.messages = prune_large_messages(run_input.messages)

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        return StreamingResponse(
            adapter.encode_stream(adapter.run_stream()), media_type=accept
        )

    if enable_web_ui:
        app.mount("/", agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT))

    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


def agent_server():
    print(f"Jellyfin Agent v{__version__}")
    parser = argparse.ArgumentParser(
        description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument("--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["openai", "anthropic", "google", "huggingface"],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_OPENAI_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_OPENAI_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )
    args = parser.parse_args()

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
    )


if __name__ == "__main__":
    agent_server()
