"""The connector ontology must not redeclare a class the core ontology owns."""

from __future__ import annotations

import re
from importlib import resources

import pytest


@pytest.mark.spec("CONN-JELLYFIN-MCP-CONNECTOR-CONTENT-R002")
def test_no_duplicate_class_iri_with_core() -> None:
    text = (
        resources.files("jellyfin_mcp.ontology")
        .joinpath("media.ttl")
        .read_text(encoding="utf-8")
    )
    assert not re.search(r"^:Author\s+a\s+owl:Class", text, re.M)
    assert "core:Author" not in text
    block = re.search(r"^:authoredBy\s.*?\.\s*$", text, re.M | re.S)
    assert block is not None
    assert "rdfs:subPropertyOf mv:contributor" in block.group(0)
    assert "rdfs:range core:Person" in block.group(0)
