from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from bizverify_agents._base import BizVerifyClient


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BIZVERIFY_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key is required"):
        BizVerifyClient()


def test_client_reads_env_var(monkeypatch: pytest.MonkeyPatch, mock_bizverify_sdk: MagicMock) -> None:
    monkeypatch.setenv("BIZVERIFY_API_KEY", "bv_env_key")
    client = BizVerifyClient()
    assert client is not None


def test_client_prefers_constructor_key(monkeypatch: pytest.MonkeyPatch, mock_bizverify_sdk: MagicMock) -> None:
    monkeypatch.setenv("BIZVERIFY_API_KEY", "bv_env_key")
    # Should not raise — constructor key takes priority
    client = BizVerifyClient(api_key="bv_constructor_key")
    assert client is not None


def test_run_tool_unknown_tool(client: BizVerifyClient) -> None:
    result = client.run_tool("nonexistent_tool")
    assert "Error: Unknown tool" in result
    assert "nonexistent_tool" in result


def test_run_tool_get_account(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakeAccount:
        email: str = "test@example.com"
        credit_balance: int = 100
        plan: str = "free"

    mock_bizverify_sdk.account.get.return_value = FakeAccount()
    result = client.run_tool("get_account")
    assert "Account" in result
    assert "test@example.com" in result
    assert "100" in result
    mock_bizverify_sdk.account.get.assert_called_once()


def test_run_tool_verify_business(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakeVerifyResponse:
        job_id: str = "job-123"
        status: str = "pending"

    mock_bizverify_sdk.verification.verify.return_value = FakeVerifyResponse()
    result = client.run_tool("verify_business", entity_name="Acme Corp", jurisdiction="us-fl")
    assert "Verification submitted" in result
    assert "job-123" in result
    mock_bizverify_sdk.verification.verify.assert_called_once_with(
        "Acme Corp", "us-fl", verification_level="full", force_refresh=None, webhook_url=None,
    )


def test_run_tool_search_entities(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakeResult:
        name: str = "Acme Corp"
        jurisdiction: str = "us-fl"

    @dataclass(frozen=True)
    class FakeSearchResponse:
        results: list = None  # type: ignore[assignment]

        def __post_init__(self) -> None:
            object.__setattr__(self, "results", [FakeResult()])

    mock_bizverify_sdk.search.find.return_value = FakeSearchResponse()
    result = client.run_tool("search_entities", query="Acme")
    assert "Search results" in result
    assert "Acme Corp" in result


def test_run_tool_handles_sdk_errors(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    from bizverify import BizVerifyError

    mock_bizverify_sdk.account.get.side_effect = BizVerifyError(
        message="Invalid API key", code="INVALID_API_KEY", status_code=401,
    )
    result = client.run_tool("get_account")
    assert "Error (INVALID_API_KEY)" in result
    assert "Invalid API key" in result


def test_run_tool_get_config(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakeConfig:
        version: str = "1.0"

    mock_bizverify_sdk.config.get.return_value = FakeConfig()
    result = client.run_tool("get_config")
    assert "Configuration" in result


def test_run_tool_list_jurisdictions(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakeJurisdiction:
        code: str = "us-fl"
        name: str = "Florida"

    @dataclass(frozen=True)
    class FakeResponse:
        jurisdictions: list = None  # type: ignore[assignment]

        def __post_init__(self) -> None:
            object.__setattr__(self, "jurisdictions", [FakeJurisdiction()])

    mock_bizverify_sdk.config.jurisdictions.return_value = FakeResponse()
    result = client.run_tool("list_jurisdictions")
    assert "Jurisdictions" in result
    assert "Florida" in result


def test_run_tool_purchase_credits(client: BizVerifyClient, mock_bizverify_sdk: MagicMock) -> None:
    @dataclass(frozen=True)
    class FakePurchase:
        checkout_url: str = "https://checkout.stripe.com/123"

    mock_bizverify_sdk.billing.purchase.return_value = FakePurchase()
    result = client.run_tool("purchase_credits", package_id="pkg-100")
    assert "Purchase" in result
    assert "checkout.stripe.com" in result
    mock_bizverify_sdk.billing.purchase.assert_called_once_with("pkg-100")
