from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from bizverify_agents._base import BizVerifyClient


@pytest.fixture
def mock_bizverify_sdk(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    monkeypatch.setattr("bizverify_agents._base.BizVerify", lambda **_kw: mock)
    return mock


@pytest.fixture
def client(mock_bizverify_sdk: MagicMock) -> BizVerifyClient:
    return BizVerifyClient(api_key="bv_test_123")
