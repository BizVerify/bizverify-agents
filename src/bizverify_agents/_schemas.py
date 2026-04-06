from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolParam:
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: list[str] | None = None


@dataclass(frozen=True)
class ToolSchema:
    name: str
    title: str
    description: str
    params: list[ToolParam] = field(default_factory=list)


TOOLS: list[ToolSchema] = [
    ToolSchema(
        name="verify_business",
        title="verify_business",
        description=(
            "Verify a business entity against official government registries. "
            'Costs 1 credit (pre_check), 15 credits (full), or 25 credits (full + force_refresh).'
        ),
        params=[
            ToolParam(name="entity_name", type="string", description="Business entity name to verify"),
            ToolParam(
                name="jurisdiction",
                type="string",
                description='Jurisdiction code or name (e.g., "us-fl", "Florida", "FL")',
            ),
            ToolParam(
                name="level",
                type="string",
                description="Verification level",
                required=False,
                default="full",
                enum=["pre_check", "full"],
            ),
            ToolParam(
                name="force_refresh",
                type="boolean",
                description="Force fresh data from government registry",
                required=False,
                default=False,
            ),
            ToolParam(
                name="webhook_url",
                type="string",
                description="URL to receive async results",
                required=False,
            ),
        ],
    ),
    ToolSchema(
        name="search_entities",
        title="search_entities",
        description="Search for business entities across jurisdictions. Costs 2 credits per jurisdiction searched.",
        params=[
            ToolParam(name="query", type="string", description="Business name search query"),
            ToolParam(
                name="jurisdiction",
                type="string",
                description="Jurisdiction code or name (omit to search all active)",
                required=False,
            ),
            ToolParam(
                name="entity_type",
                type="string",
                description="Filter by entity type",
                required=False,
            ),
            ToolParam(
                name="limit",
                type="integer",
                description="Maximum number of results to return",
                required=False,
                default=10,
            ),
            ToolParam(
                name="offset",
                type="integer",
                description="Number of results to skip",
                required=False,
                default=0,
            ),
        ],
    ),
    ToolSchema(
        name="check_job_status",
        title="check_job_status",
        description="Poll an async verification job. Free — no credits charged.",
        params=[
            ToolParam(name="job_id", type="string", description="Job ID from verify_business async response"),
        ],
    ),
    ToolSchema(
        name="get_entity",
        title="get_entity",
        description="Retrieve cached entity data by ID. Free — no credits charged.",
        params=[
            ToolParam(name="entity_id", type="string", description="Entity ID from verify or search results"),
        ],
    ),
    ToolSchema(
        name="get_entity_history",
        title="get_entity_history",
        description="Get historical verification snapshots for an entity. Costs 1 credit.",
        params=[
            ToolParam(name="entity_id", type="string", description="Entity ID to retrieve history for"),
            ToolParam(
                name="limit",
                type="integer",
                description="Maximum number of snapshots to return",
                required=False,
                default=10,
            ),
            ToolParam(
                name="offset",
                type="integer",
                description="Number of snapshots to skip",
                required=False,
                default=0,
            ),
        ],
    ),
    ToolSchema(
        name="get_account",
        title="get_account",
        description="Returns account details including credit balance and API keys.",
        params=[],
    ),
    ToolSchema(
        name="get_config",
        title="get_config",
        description=(
            "Returns public configuration including supported jurisdictions, "
            "credit pricing, available packages, and features."
        ),
        params=[],
    ),
    ToolSchema(
        name="list_jurisdictions",
        title="list_jurisdictions",
        description="Returns all registered jurisdictions with scraper capabilities and active status.",
        params=[],
    ),
    ToolSchema(
        name="purchase_credits",
        title="purchase_credits",
        description=(
            "Creates a Stripe checkout session and returns a payment URL. "
            "Present the URL to the user to complete payment."
        ),
        params=[
            ToolParam(name="package_id", type="string", description="Package ID from get_config pricing section"),
        ],
    ),
]

TOOL_MAP: dict[str, ToolSchema] = {t.name: t for t in TOOLS}
