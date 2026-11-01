# CONN-JELLYFIN-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-JELLYFIN-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |

## Rows awaiting bound tests
- `CONN-JELLYFIN-MCP-CONNECTOR-CONTENT-R002`: planned proof `tests/test_ontology_namespace.py::test_no_duplicate_class_iri_with_core`. Expected: Loading the media ontology with core yields no class IRI declared twice, and Book authors use mv:contributor to :Person.. Refusal: Re-adding a :Author class in the shared namespace makes the duplicate-IRI check fail..
