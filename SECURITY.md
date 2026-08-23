# Security Policy

## Reporting a Vulnerability

If you believe you've found a security issue in this plugin or in the TranscriptAPI service, email
**hello@transcriptapi.com**. Please do not open a public issue for security reports.

We aim to acknowledge reports within 2 business days.

## Scope

- This repository contains **only** plugin metadata, skill markdown, and an MCP client configuration
  pointing at the hosted server `https://transcriptapi.com/mcp`.
- It contains **no secrets and no executable code**. Agent Plugins 1.0.0 has no portable field for
  embedding credentials, and this package ships none.
- Authorization is client-managed: your agent authenticates over MCP OAuth 2.1 (Dynamic Client
  Registration) directly against TranscriptAPI, or you supply your own API key via your client's
  own configuration. Neither is stored in this repository.
- Every path shipped in this package resolves inside the plugin root. There are no symlinks and no
  `stdio` MCP servers, so nothing in this package executes on your machine.

## Verify this package yourself

```bash
# 1. manifests against the canonical schemas
curl -sO https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
curl -sO https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
npx -y ajv-cli@5 validate --spec=draft2020 -s plugin.schema.json -d plugin.json
npx -y ajv-cli@5 validate --spec=draft2020 -s mcp.schema.json    -d mcp.json

# 2. every skill against the Agent Skills specification (Agent Plugins §7.1)
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
for d in skills/*/; do skills-ref validate "$d"; done

# 3. normative requirements a schema cannot express
python .github/scripts/check_conformance.py
```

All three must pass. CI runs exactly this on every push and weekly on a schedule — see
[`.github/workflows/validate-plugin.yml`](.github/workflows/validate-plugin.yml).
