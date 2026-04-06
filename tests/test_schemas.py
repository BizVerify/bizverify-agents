from __future__ import annotations

from bizverify_agents._schemas import TOOL_MAP, TOOLS


def test_tools_count() -> None:
    assert len(TOOLS) == 9


def test_tool_map_matches_tools() -> None:
    assert len(TOOL_MAP) == len(TOOLS)
    for tool in TOOLS:
        assert tool.name in TOOL_MAP
        assert TOOL_MAP[tool.name] is tool


def test_all_tools_have_descriptions() -> None:
    for tool in TOOLS:
        assert tool.description
        assert tool.title


def test_verify_business_has_required_params() -> None:
    schema = TOOL_MAP["verify_business"]
    required = [p for p in schema.params if p.required]
    names = {p.name for p in required}
    assert "entity_name" in names
    assert "jurisdiction" in names


def test_search_entities_has_query_param() -> None:
    schema = TOOL_MAP["search_entities"]
    required = [p for p in schema.params if p.required]
    assert any(p.name == "query" for p in required)


def test_no_params_tools() -> None:
    for name in ("get_account", "get_config", "list_jurisdictions"):
        schema = TOOL_MAP[name]
        assert len(schema.params) == 0
