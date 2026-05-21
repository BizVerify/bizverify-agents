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
            "Confirm a specific, named business in one jurisdiction — the PRIMARY tool "
            "whenever the user wants to verify, check, confirm, or look up a company's "
            "existence, status, good standing, or details (e.g. 'verify Acme LLC in "
            "Delaware', 'is Acme registered in FL?', 'I need to verify a company in "
            "Delaware'). If the user has verification intent but has not given the exact "
            "company name, ASK them for the name and use THIS tool — do NOT fall back to "
            "search_entities. Two tiers — quick (1 credit): existence + status + good "
            "standing. Deep (15 credits, 25 with force_refresh): adds entity type, "
            "formation date, registered agent, officers, principal address, and filing "
            "history. Deep is available in a subset of jurisdictions; requesting deep "
            "where unavailable returns quick with a reason."
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
                description="Verification tier: 'quick' or 'deep'",
                required=False,
                default="quick",
                enum=["quick", "deep"],
            ),
            ToolParam(
                name="force_refresh",
                type="boolean",
                description="Bypass cache and fetch fresh data",
                required=False,
                default=False,
            ),
            ToolParam(
                name="webhook_url",
                type="string",
                description="URL to receive async results",
                required=False,
            ),
            ToolParam(
                name="entity_type",
                type="string",
                description="Optional entity type hint (e.g. 'LLC', 'Corporation'). Helps disambiguate results.",
                required=False,
            ),
        ],
    ),
    ToolSchema(
        name="search_entities",
        title="search_entities",
        description=(
            "Discover candidate businesses when the exact entity is UNKNOWN — a "
            "listing/discovery tool, NOT a verification tool. Use only when the user "
            "wants to browse or list multiple companies matching a partial or fuzzy "
            "name, or does not yet know which specific entity they mean. If the user can "
            "name one specific company they want to confirm or check, use verify_business "
            "instead (ask them for the name first if needed). Costs 2 credits per "
            "jurisdiction searched."
        ),
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
                default=50,
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
        description="Get historical verification snapshots for an entity. Costs 5 credits.",
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
        description="Returns all registered jurisdictions with supported capabilities and active status.",
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
