#!/usr/bin/env python3
"""Read-only entry point for canvas-ed-mcp.

This entry point imports the normal server and removes every MCP tool whose
annotations do not declare it read-only. The filtering happens before the
server starts, so write-capable tools are not advertised to MCP clients at all.

Use canvas_ed_mcp.py when write access is intentionally required.
"""

from canvas_ed_mcp import mcp


def _remove_non_readonly_tools() -> None:
    """Remove tools that are not explicitly annotated read-only."""
    tool_manager = getattr(mcp, "_tool_manager", None)
    tools = getattr(tool_manager, "_tools", None)
    if not isinstance(tools, dict):
        raise RuntimeError(
            "Unsupported MCP SDK: FastMCP tool registry is unavailable. "
            "Refusing to start because read-only isolation cannot be guaranteed."
        )

    for name, tool in list(tools.items()):
        annotations = getattr(tool, "annotations", None)
        read_only = getattr(annotations, "readOnlyHint", None)
        if read_only is None and isinstance(annotations, dict):
            read_only = annotations.get("readOnlyHint")

        # Fail closed: only explicitly read-only tools survive.
        if read_only is not True:
            tools.pop(name, None)


if __name__ == "__main__":
    _remove_non_readonly_tools()
    mcp.run()
