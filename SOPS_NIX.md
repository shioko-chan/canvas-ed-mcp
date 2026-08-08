# sops-nix credential setup

The MCP can consume credentials from files, which is the recommended setup on NixOS. Secret values do not need to appear in the MCP client JSON or Nix store.

## Supported variables

For each credential, the `*_FILE` form is preferred when set; the original environment-variable setup remains compatible.

- `CANVAS_API_TOKEN_FILE`
- `ED_API_TOKEN_FILE`
- `GRADESCOPE_EMAIL_FILE`
- `GRADESCOPE_PASSWORD_FILE`

The files should contain only the corresponding credential value (a trailing newline is fine).

## 1. Store encrypted secrets with SOPS

Example plaintext shape while editing with `sops secrets.yaml`:

```yaml
canvas_api_token: "..."
ed_api_token: "..."
gradescope_email: "..."
gradescope_password: "..."
```

After saving, SOPS encrypts the values. Commit only the encrypted `secrets.yaml`; never commit the age private key or plaintext credentials.

## 2. Declare the secrets in NixOS

Assuming sops-nix is already imported:

```nix
{ config, ... }:
{
  sops.defaultSopsFile = ./secrets.yaml;
  sops.defaultSopsFormat = "yaml";

  sops.secrets.canvas_api_token = {
    owner = "YOUR_USER";
    mode = "0400";
  };
  sops.secrets.ed_api_token = {
    owner = "YOUR_USER";
    mode = "0400";
  };
  sops.secrets.gradescope_email = {
    owner = "YOUR_USER";
    mode = "0400";
  };
  sops.secrets.gradescope_password = {
    owner = "YOUR_USER";
    mode = "0400";
  };
}
```

sops-nix exposes these as runtime files (normally under `/run/secrets`). Use `config.sops.secrets.<name>.path` instead of hard-coding the generated path when possible.

## 3. Point the MCP process at the files

Set only file paths in the MCP client configuration:

```json
{
  "mcpServers": {
    "canvas-ed-read": {
      "command": "python",
      "args": ["/path/to/canvas-ed-mcp/canvas_ed_mcp_readonly.py"],
      "env": {
        "CANVAS_API_TOKEN_FILE": "/run/secrets/canvas_api_token",
        "ED_API_TOKEN_FILE": "/run/secrets/ed_api_token",
        "GRADESCOPE_EMAIL_FILE": "/run/secrets/gradescope_email",
        "GRADESCOPE_PASSWORD_FILE": "/run/secrets/gradescope_password"
      }
    }
  }
}
```

For the full read-write server with file-backed credentials, use `canvas_ed_mcp_sops.py` instead.

## Credential precedence

If both forms are configured, `NAME_FILE` wins over `NAME`. This makes migration safe while ensuring the sops-nix value is the one actually used.

The loader reads each file immediately before importing the existing server module. The original `canvas_ed_mcp.py` remains compatible with its existing environment-variable configuration for non-Nix users.
