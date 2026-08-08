# Read / write permission split

This fork provides two MCP entry points so clients can be given least-privilege access.

## Read-only server (recommended default)

Run:

```bash
python /path/to/canvas-ed-mcp/canvas_ed_mcp_readonly.py
```

The read-only entry point installs a guarded `FastMCP` class **before** importing the main server module. As the existing `@mcp.tool(...)` decorators execute, only tools explicitly annotated with `readOnlyHint=True` are registered. Write-capable and unannotated functions are still valid internal Python functions, but they never enter the MCP tool registry and therefore cannot be advertised or called by the MCP client.

This avoids inspecting or mutating FastMCP's private `_tool_manager` / `_tools` internals.

Example client configuration:

```json
{
  "mcpServers": {
    "canvas-ed-read": {
      "command": "python",
      "args": ["/path/to/canvas-ed-mcp/canvas_ed_mcp_readonly.py"],
      "env": {
        "CANVAS_API_TOKEN": "...",
        "ED_API_TOKEN": "...",
        "GRADESCOPE_EMAIL": "...",
        "GRADESCOPE_PASSWORD": "..."
      }
    }
  }
}
```

This mode excludes Canvas submission/discussion posting, Ed posting/editing/actions, workspace mutations, and local download tools currently marked non-read-only.

## Read-write server

Run the original entry point:

```bash
python /path/to/canvas-ed-mcp/canvas_ed_mcp.py
```

Example client configuration:

```json
{
  "mcpServers": {
    "canvas-ed-write": {
      "command": "python",
      "args": ["/path/to/canvas-ed-mcp/canvas_ed_mcp.py"],
      "env": {
        "CANVAS_API_TOKEN": "...",
        "ED_API_TOKEN": "...",
        "GRADESCOPE_EMAIL": "...",
        "GRADESCOPE_PASSWORD": "..."
      }
    }
  }
}
```

Keep this server disabled unless a write operation is intentionally needed. MCP client confirmation prompts remain useful, but the read-only server provides the stronger boundary because mutating tools are absent from its advertised tool set.

## Security model

The split is based on each tool's MCP `readOnlyHint` annotation and uses a fail-closed allowlist policy:

- `readOnlyHint=True` -> registered by the read-only MCP server.
- `readOnlyHint=False` -> not registered.
- missing/unknown annotation -> not registered.

The filtering happens at decoration/registration time, not after server construction. New tools therefore default to unavailable in read-only mode until their annotation is reviewed.

The original `canvas_ed_mcp.py` is unchanged and remains the intentional full read-write entry point.
