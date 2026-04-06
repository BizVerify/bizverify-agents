from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bizverify_agents._schemas import TOOLS


@pytest.fixture
def mock_sdk() -> MagicMock:
    return MagicMock()


@pytest.fixture
def tools(mock_sdk: MagicMock) -> list:
    with patch("bizverify_agents._base.BizVerify", return_value=mock_sdk):
        from bizverify_agents.langchain.tools import BizVerifyTools

        bv = BizVerifyTools(api_key="bv_test_123")
        return bv.get_tools()


def test_get_tools_returns_all_nine(tools: list) -> None:
    assert len(tools) == 9


def test_tools_are_langchain_base_tools(tools: list) -> None:
    from langchain_core.tools import BaseTool

    for tool in tools:
        assert isinstance(tool, BaseTool)


def test_tool_has_description(tools: list) -> None:
    for tool in tools:
        assert tool.description
        assert len(tool.description) > 10


def test_tool_names_match_schemas(tools: list) -> None:
    expected_names = {t.name for t in TOOLS}
    actual_names = {t.name for t in tools}
    assert actual_names == expected_names


def test_verify_business_tool_invokes_client(mock_sdk: MagicMock) -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FakeResp:
        job_id: str = "job-1"
        status: str = "pending"

    mock_sdk.verification.verify.return_value = FakeResp()

    with patch("bizverify_agents._base.BizVerify", return_value=mock_sdk):
        from bizverify_agents.langchain.tools import BizVerifyTools

        bv = BizVerifyTools(api_key="bv_test_123")
        tool_list = bv.get_tools()
        verify_tool = next(t for t in tool_list if t.name == "verify_business")

        result = verify_tool.invoke({"entity_name": "Acme Corp", "jurisdiction": "us-fl"})
        assert "job-1" in result
        mock_sdk.verification.verify.assert_called_once()


def test_tool_with_no_params(mock_sdk: MagicMock) -> None:
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FakeConfig:
        version: str = "1.0"

    mock_sdk.config.get.return_value = FakeConfig()

    with patch("bizverify_agents._base.BizVerify", return_value=mock_sdk):
        from bizverify_agents.langchain.tools import BizVerifyTools

        bv = BizVerifyTools(api_key="bv_test_123")
        tool_list = bv.get_tools()
        config_tool = next(t for t in tool_list if t.name == "get_config")

        result = config_tool.invoke({})
        assert "Configuration" in result
