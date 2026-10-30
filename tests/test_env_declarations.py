"""The shipped env declarations match the env surface the code reads."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.spec("CONN-JELLYFIN-MCP-R002")
def test_env_declarations_match_the_code_read_surface():
    result = subprocess.run(
        [sys.executable, "-m", "scion_sdk.mcp.env_drift", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
