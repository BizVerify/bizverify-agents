from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any

from bizverify import BizVerify, BizVerifyError

from bizverify_agents._schemas import TOOL_MAP


def _format_dataclass(obj: Any) -> str:
    """Format a dataclass instance as a readable string."""
    try:
        d = asdict(obj)
    except TypeError:
        return str(obj)
    lines: list[str] = []
    for key, value in d.items():
        if value is not None:
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def _format_result(label: str, obj: Any) -> str:
    """Format a result object with a label header."""
    return f"{label}:\n{_format_dataclass(obj)}"


def _format_list(label: str, items: list[Any], item_label: str = "Item") -> str:
    """Format a list of dataclass items."""
    if not items:
        return f"{label}: (none)"
    parts = [f"{label} ({len(items)} results):"]
    for i, item in enumerate(items, 1):
        parts.append(f"\n{item_label} {i}:")
        parts.append(_format_dataclass(item))
    return "\n".join(parts)


class BizVerifyClient:
    """Thin wrapper around the BizVerify Python SDK, dispatching tool calls by name."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("BIZVERIFY_API_KEY")
        if not resolved_key:
            raise ValueError(
                "BizVerify API key is required. Pass api_key= or set the BIZVERIFY_API_KEY environment variable."
            )
        kwargs: dict[str, Any] = {"api_key": resolved_key}
        if base_url is not None:
            kwargs["base_url"] = base_url
        self._sdk = BizVerify(**kwargs)

    def run_tool(self, tool_name: str, **kwargs: Any) -> str:
        """Dispatch a tool call to the appropriate SDK method and return a human-readable string."""
        if tool_name not in TOOL_MAP:
            return f"Error: Unknown tool '{tool_name}'. Available tools: {', '.join(TOOL_MAP.keys())}"
        try:
            return self._dispatch(tool_name, **kwargs)
        except BizVerifyError as exc:
            return f"Error ({exc.code}): {exc.message}"

    def _dispatch(self, tool_name: str, **kwargs: Any) -> str:
        if tool_name == "verify_business":
            return self._verify_business(**kwargs)
        if tool_name == "search_entities":
            return self._search_entities(**kwargs)
        if tool_name == "check_job_status":
            return self._check_job_status(**kwargs)
        if tool_name == "get_entity":
            return self._get_entity(**kwargs)
        if tool_name == "get_entity_history":
            return self._get_entity_history(**kwargs)
        if tool_name == "get_account":
            return self._get_account()
        if tool_name == "get_config":
            return self._get_config()
        if tool_name == "list_jurisdictions":
            return self._list_jurisdictions()
        if tool_name == "purchase_credits":
            return self._purchase_credits(**kwargs)
        return f"Error: Tool '{tool_name}' is not implemented."

    def _verify_business(
        self,
        entity_name: str,
        jurisdiction: str,
        level: str = "full",
        force_refresh: bool = False,
        webhook_url: str | None = None,
    ) -> str:
        resp = self._sdk.verification.verify(
            entity_name,
            jurisdiction,
            verification_level=level,
            force_refresh=force_refresh or None,
            webhook_url=webhook_url,
        )
        return _format_result("Verification submitted", resp)

    def _search_entities(
        self,
        query: str,
        jurisdiction: str | None = None,
        entity_type: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> str:
        resp = self._sdk.search.find(
            query,
            jurisdiction=jurisdiction,
            entity_type=entity_type,
            limit=limit,
            offset=offset,
        )
        results = resp.results if hasattr(resp, "results") else []
        return _format_list("Search results", list(results), "Entity")

    def _check_job_status(self, job_id: str) -> str:
        resp = self._sdk.verification.get_status(job_id)
        return _format_result("Job status", resp)

    def _get_entity(self, entity_id: str) -> str:
        resp = self._sdk.entities.get(entity_id)
        return _format_result("Entity", resp)

    def _get_entity_history(
        self,
        entity_id: str,
        limit: int = 10,
        offset: int = 0,
    ) -> str:
        resp = self._sdk.entities.history(entity_id, limit=limit, offset=offset)
        snapshots = resp.snapshots if hasattr(resp, "snapshots") else []
        return _format_list("Entity history", list(snapshots), "Snapshot")

    def _get_account(self) -> str:
        resp = self._sdk.account.get()
        return _format_result("Account", resp)

    def _get_config(self) -> str:
        resp = self._sdk.config.get()
        return _format_result("Configuration", resp)

    def _list_jurisdictions(self) -> str:
        resp = self._sdk.config.jurisdictions()
        jurisdictions = resp.jurisdictions if hasattr(resp, "jurisdictions") else []
        return _format_list("Jurisdictions", list(jurisdictions), "Jurisdiction")

    def _purchase_credits(self, package_id: str) -> str:
        resp = self._sdk.billing.purchase(package_id)
        return _format_result("Purchase", resp)
