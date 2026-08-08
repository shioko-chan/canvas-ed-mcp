#!/usr/bin/env python3
"""Read-only entry point for canvas-ed-mcp.

Only tools explicitly annotated with readOnlyHint=True are registered with
FastMCP. Write-capable or unannotated tools never enter the MCP tool registry.

Use canvas_ed_mcp.py when write access is intentionally required.
"""

from readonly_fastmcp import install_readonly_fastmcp

# This must happen before importing canvas_ed_mcp because its @mcp.tool
# decorators execute during module import.
install_readonly_fastmcp()

from canvas_ed_mcp import mcp  # noqa: E402


if __name__ == "__main__":
    mcp.run()
