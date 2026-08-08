"""Load MCP credentials from secret files without exposing values in config.

For each credential, NAME_FILE takes precedence over the legacy NAME
environment variable. This is designed for sops-nix paths under /run/secrets,
while keeping existing non-Nix setups compatible.
"""

import os
from pathlib import Path

CREDENTIAL_NAMES = (
    "CANVAS_API_TOKEN",
    "ED_API_TOKEN",
    "GRADESCOPE_EMAIL",
    "GRADESCOPE_PASSWORD",
)


def install_file_credentials() -> None:
    """Resolve *_FILE credentials and place values in this process environment.

    canvas_ed_mcp currently reads its configuration from environment variables
    during import. This loader runs immediately before that import. Secret values
    are not required in the MCP client configuration; only file paths are.
    """
    for name in CREDENTIAL_NAMES:
        file_path = os.getenv(f"{name}_FILE")
        if not file_path:
            continue

        try:
            value = Path(file_path).read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise RuntimeError(
                f"Unable to read credential file configured by {name}_FILE: {file_path}"
            ) from exc

        os.environ[name] = value
