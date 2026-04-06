from __future__ import annotations

from typing import Any, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from bizverify_agents._base import BizVerifyClient
from bizverify_agents._schemas import TOOLS, ToolSchema

_TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "boolean": bool,
}


def _build_args_schema(schema: ToolSchema) -> Type[BaseModel]:
    """Dynamically build a Pydantic model from a ToolSchema's params."""
    field_definitions: dict[str, Any] = {}
    for param in schema.params:
        py_type = _TYPE_MAP.get(param.type, str)
        if param.required:
            field_definitions[param.name] = (py_type, Field(description=param.description))
        else:
            field_definitions[param.name] = (
                py_type | None,
                Field(default=param.default, description=param.description),
            )

    namespace: dict[str, Any] = {"__annotations__": {}}
    for name, (type_, field_info) in field_definitions.items():
        namespace["__annotations__"][name] = type_
        namespace[name] = field_info

    return type(f"{schema.name}_input", (BaseModel,), namespace)


def _make_tool(schema: ToolSchema, client: BizVerifyClient) -> BaseTool:
    """Create a CrewAI BaseTool subclass for a given ToolSchema."""
    args_model = _build_args_schema(schema)

    tool_name = schema.name
    tool_description = schema.description

    class DynamicTool(BaseTool):
        name: str = tool_name  # type: ignore[assignment]
        description: str = tool_description
        args_schema: Type[BaseModel] = args_model

        def _run(self, **kwargs: Any) -> str:
            filtered = {k: v for k, v in kwargs.items() if v is not None}
            return client.run_tool(tool_name, **filtered)

    return DynamicTool()


class BizVerifyTools:
    """Factory for CrewAI-compatible BizVerify tools."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._client = BizVerifyClient(api_key=api_key, base_url=base_url)

    def get_tools(self) -> list[BaseTool]:
        """Return all 9 BizVerify tools as CrewAI BaseTool instances."""
        return [_make_tool(schema, self._client) for schema in TOOLS]
