# Read / write permission split

This fork provides two MCP entry points so clients can be given least-privilege access.

## Read-only server (recommended default)

Run:

```bash
python /path/to/canvas-ed-mcp/canvas_ed_mcp_readonly.py
```

The read-only entry point imports the normal server and then removes every tool that is not explicitly annotated with `readOnlyHint=True` **before** starting MCP. It fails closed if the MCP SDK tool registry cannot be inspected, rather than accidentally exposing write tools.

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

The split is based on each tool's MCP `readOnlyHint` annotation and uses a fail-closed policy: a tool is exposed by the read-only server only when it is explicitly marked read-only. New tools therefore default to unavailable in read-only mode until their annotation is reviewed.
