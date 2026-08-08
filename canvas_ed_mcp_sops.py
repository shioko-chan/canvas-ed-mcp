#!/usr/bin/env python3
"""Read-write MCP entry point for file-backed/sops-nix credentials."""

from credential_loader import install_file_credentials

# Resolve /run/secrets-style files before canvas_ed_mcp reads configuration.
install_file_credentials()

from canvas_ed_mcp import mcp  # noqa: E402


if __name__ == "__main__":
    mcp.run()
