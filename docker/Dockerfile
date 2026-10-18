# syntax=docker/dockerfile:1
# MCP serving image. It installs the published jellyfin-mcp wheel from PyPI at the
# pinned version (tracked by .bumpversion.cfg), never the source tree, and
# builds no tools from source.
#
#   docker build --file docker/Dockerfile --target mcp -t jellyfin-mcp:<version>-mcp .
FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6 AS mcp
ARG HOST=127.0.0.1
ARG PORT=8000
ARG TRANSPORT="stdio"
ARG AUTH_TYPE="none"
ENV HOST=${HOST} \
    PORT=${PORT} \
    TRANSPORT=${TRANSPORT} \
    AUTH_TYPE=${AUTH_TYPE} \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOME=/tmp \
    XDG_CONFIG_HOME=/tmp/.config \
    XDG_CACHE_HOME=/tmp/.cache
# Fixed identity for least-privilege runtime and stable volume ownership.
RUN pip install --only-binary :all: jellyfin-mcp[mcp]==2.3.0 \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid 10001 --no-create-home \
        --home-dir /tmp --shell /usr/sbin/nologin app
USER 10001:10001
CMD ["jellyfin-mcp"]

FROM mcp AS default
