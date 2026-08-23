# Contributing

PRs welcome. This repository is an [Agent Plugins 1.0.0](https://agent-plugins.org/specification) package,
so the bar for a merge is: **both manifests still validate, and every skill still has valid frontmatter.**
CI enforces exactly that on every pull request.

## Before you open a PR

```bash
# manifests
curl -sO https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
curl -sO https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
npx -y ajv-cli@5 validate --spec=draft2020 -s plugin.schema.json -d plugin.json
npx -y ajv-cli@5 validate --spec=draft2020 -s mcp.schema.json    -d mcp.json

# skills — the check that actually matters (see below)
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
for d in skills/*/; do skills-ref validate "$d"; done

# everything a schema can't express
python .github/scripts/check_conformance.py
```

All must pass.

> **Why the skills check matters most.** Agent Plugins §7.1 requires every skill to conform to the
> [Agent Skills specification](https://agentskills.io/specification), and a conformant client
> **silently skips** any skill that doesn't. A schema-valid `plugin.json` with a bad `SKILL.md`
> produces a plugin that installs cleanly and then does nothing. Never hand-roll this check —
> `skills-ref` is the official reference validator.

## Adding a new skill

1. Create a folder in `skills/` — lowercase, hyphens only. It must be an *immediate* child of `skills/`;
   the spec does not search recursively.
2. Add `SKILL.md` with YAML frontmatter. **The frontmatter schema is closed** — the only permitted fields
   are `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. `name` and
   `description` are required, and `name` MUST match the directory name exactly.
   - `metadata` is a flat map of **string keys to string values**. Nest nothing. Anything runtime-specific
     (OpenClaw, Hermes, versioning, required env vars) goes here as flat prefixed keys — see any existing
     skill for the pattern.
   - The parser is `strictyaml`, which rejects JSON-style flow mappings (`{"a": 1}`). Use block style and
     quote your values.
   - Limits: `name` ≤ 64 chars, `description` ≤ 1024, `compatibility` ≤ 500.
3. Write the `description` as **trigger vocabulary** — the phrases a user would actually type. It's the only
   thing the agent sees when deciding whether to load your skill, so it matters more than the body.
4. Put long-form detail in `references/` (e.g. `references/auth-setup.md`, `references/curl-examples.md`)
   rather than inflating `SKILL.md`. Smaller skill bodies = better agent performance.
5. Open the PR.

## Improving existing skills

- Better trigger phrases in `description`
- Clearer or more accurate examples
- Corrections to endpoints, parameters, error codes or credit costs

If you change a skill's API surface, update the matching section of the README table too.

## Changing manifests

`plugin.json` validates with `additionalProperties: false` — only the ten spec fields are allowed
(`$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`,
`extensions`). Anything vendor-specific belongs under `extensions` in a reverse-domain namespace, or in the
per-client manifests under `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/` and `.plugin/`.

Keep the per-client manifests in sync with the root manifest when you bump the version.

## Quality checklist

- [ ] `plugin.json` and `mcp.json` both validate against the canonical schemas
- [ ] Every `skills/*/SKILL.md` exists and opens with YAML frontmatter
- [ ] Description includes real when-to-use phrases
- [ ] No secrets, no API keys, no executable code committed
- [ ] Tested locally with your client (or `npx skills add` for the skills-only path)

## Questions?

Open an issue or reach out at [transcriptapi.com](https://transcriptapi.com).
