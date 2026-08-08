"""Registration-time read-only FastMCP guard.

The normal canvas_ed_mcp module decorates all tools as it is imported. For the
read-only entry point we replace FastMCP before that import so only tools that
explicitly declare readOnlyHint=True are ever registered.

This deliberately fails closed: unannotated tools and tools marked non-read-only
remain ordinary Python callables, but are never exposed through MCP.
"""

from typing import Any, Callable

import mcp.server.fastmcp as fastmcp_module
from mcp.server.fastmcp import FastMCP as _FastMCP


class ReadOnlyFastMCP(_FastMCP):
    """FastMCP variant that registers only explicitly read-only tools."""

    def tool(self, *args: Any, **kwargs: Any) -> Any:
        annotations = kwargs.get("annotations")
        read_only = None

        if isinstance(annotations, dict):
            read_only = annotations.get("readOnlyHint")
        elif annotations is not None:
            read_only = getattr(annotations, "readOnlyHint", None)

        if read_only is True:
            return super().tool(*args, **kwargs)

        # Support both @mcp.tool and @mcp.tool(...). The repository currently
        # uses the latter, but handling both keeps the guard fail-closed if the
        # decorator style changes later.
        if args and callable(args[0]) and len(args) == 1 and not kwargs:
            return args[0]

        def skip_registration(func: Callable[..., Any]) -> Callable[..., Any]:
            return func

        return skip_registration


def install_readonly_fastmcp() -> None:
    """Install the guarded FastMCP class before canvas_ed_mcp is imported."""
    fastmcp_module.FastMCP = ReadOnlyFastMCP
