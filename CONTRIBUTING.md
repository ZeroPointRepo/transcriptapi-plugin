# Contributing

PRs welcome. This repository is an [Agent Plugins 1.0.0](https://agent-plugins.org/specification) package,
so the bar for a merge is: **both manifests still validate, and every skill still has valid frontmatter.**
CI enforces exactly that on every push.

## Before you open a PR

```bash
curl -sO https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
curl -sO https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
npx -y ajv-cli@5 validate --spec=draft2020 -s plugin.schema.json -d plugin.json
npx -y ajv-cli@5 validate --spec=draft2020 -s mcp.schema.json    -d mcp.json
```

Both must print `valid`.

## Adding a new skill

1. Create a folder in `skills/` — lowercase, hyphens only. It must be an *immediate* child of `skills/`;
   the spec does not search recursively.
2. Add `SKILL.md` with YAML frontmatter. At minimum `name` and `description`; the existing skills also carry
   `version`, `user-invocable`, `compatibility`, `required_environment_variables` and a `metadata` block for
   OpenClaw/Hermes.
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
