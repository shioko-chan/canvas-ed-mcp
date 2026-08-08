#!/usr/bin/env python3
"""Read-only entry point for canvas-ed-mcp.

Only tools explicitly annotated with readOnlyHint=True are registered with
FastMCP. Write-capable or unannotated tools never enter the MCP tool registry.

Credentials may be supplied through *_FILE variables (recommended with
sops-nix) or through the legacy direct environment variables.
"""

from credential_loader import install_file_credentials
from readonly_fastmcp import install_readonly_fastmcp

# Both must happen before importing canvas_ed_mcp: credentials are read and
# @mcp.tool decorators execute during module import.
install_file_credentials()
install_readonly_fastmcp()

from canvas_ed_mcp import mcp  # noqa: E402


if __name__ == "__main__":
    mcp.run()
