<!-- mcp-name: com.transcriptapi/youtube-transcript-and-youtube-search -->

<p align="center">
  <a href="https://transcriptapi.com">
    <img src="assets/logo-512.png" width="160" height="160" alt="TranscriptAPI" />
  </a>
</p>

<h1 align="center">TranscriptAPI — YouTube for AI Agents</h1>

<p align="center">
  <b>The complete YouTube toolkit as a single Agent Plugin.</b><br/>
  6 hosted MCP tools + 13 drop-in skills — transcripts, captions, video &amp; channel search, channel browsing, playlist extraction and new-upload polling.<br/>
  One install. OAuth sign-in. No API key to manage. Free tier, no card.
</p>

<p align="center">
  <a href="https://agent-plugins.org/specification"><img src="https://img.shields.io/badge/Agent_Plugins-1.0.0-6E56CF?style=for-the-badge" alt="Agent Plugins 1.0.0"/></a>
  <a href="https://github.com/ZeroPointRepo/transcriptapi-plugin/actions/workflows/validate-plugin.yml"><img src="https://img.shields.io/github/actions/workflow/status/ZeroPointRepo/transcriptapi-plugin/validate-plugin.yml?style=for-the-badge&label=schema%20valid" alt="Schema validation"/></a>
  <a href="https://github.com/ZeroPointRepo/awesome-agent-plugins"><img src="https://img.shields.io/badge/Listed-awesome--agent--plugins-blueviolet?style=for-the-badge" alt="Listed in awesome-agent-plugins"/></a>
</p>

<p align="center">
  <a href="https://transcriptapi.com"><img src="https://img.shields.io/badge/Website-transcriptapi.com-FF3B00?style=for-the-badge" alt="Website"/></a>
  <a href="https://transcriptapi.com/docs"><img src="https://img.shields.io/badge/Docs-API_Reference-06B6D4?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Docs"/></a>
  <a href="https://transcriptapi.com/swagger"><img src="https://img.shields.io/badge/Swagger-Try_API-85EA2D?style=for-the-badge&logo=swagger&logoColor=white" alt="Swagger"/></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge" alt="MIT License"/></a>
</p>

<p align="center">
  <a href="https://cursor.com/en/install-mcp?name=transcript-api&config=eyJ1cmwiOiJodHRwczovL3RyYW5zY3JpcHRhcGkuY29tL21jcCJ9"><img alt="Install in Cursor" src="https://img.shields.io/badge/Cursor-Install-000000?style=for-the-badge&logo=cursor&logoColor=white"/></a>
  <a href="https://insiders.vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22transcript-api%22%2C%22url%22%3A%22https%3A%2F%2Ftranscriptapi.com%2Fmcp%22%7D"><img alt="Install in VS Code" src="https://img.shields.io/badge/VS_Code-Install-0098FF?style=for-the-badge&logo=visualstudiocode&logoColor=white"/></a>
</p>

> **Powering 15M+ transcripts every month** · 500K+ transcripts processed daily · 49ms median response time
> Trusted in production by [youtubetotranscript.com](https://youtubetotranscript.com) (~11M/mo) and [recapio.com](https://recapio.com) (~2.8M/mo).

---

## 🧩 What is this?

This repository root is a conformant **[Agent Plugins 1.0.0](https://agent-plugins.org/specification)** package — the open, vendor-neutral packaging standard published 2026-08-06 by Amazon, Cursor, GitHub, Microsoft, OpenAI and Vercel, with Google as a core maintainer. It bundles **MCP servers and Agent Skills** into one portable, drop-in folder that every compliant client can read.

One install gives your agent both halves:

| Component | What it does |
|---|---|
| **MCP server** (`transcriptapi`) | 6 hosted tools over streamable HTTP with OAuth 2.1 — `get_youtube_transcript`, `search_youtube`, `get_channel_latest_videos`, `search_channel_videos`, `list_channel_videos`, `list_playlist_videos`. No key handling: your agent signs you in on first use. |
| **13 skills** (`skills/`) | Teach the agent *when* to reach for YouTube data, which tool is cheapest, and how not to burn credits — plus a full REST fallback path for agents without MCP. Deliberately overlapping trigger vocabulary so the right skill fires however you phrase the request. |

**Just ask, in plain English:**

```txt
Summarize this video for me: https://youtu.be/dQw4w9WgXcQ
Find Andrew Huberman's three most-viewed videos about sleep and compare them.
What has @TED posted in the last month?
```

That last set of prompts touches 3 of the 6 tools — `search_youtube`, `search_channel_videos`, `get_youtube_transcript` — without you writing a line of code.

---

## Why TranscriptAPI

Most YouTube integrations do one thing — pull a single transcript. **This is a full toolkit.**

|                                          | TranscriptAPI | Typical YouTube MCP / skill |
| ---------------------------------------- | ----------------- | ------------------- |
| Packaging                                | ✅ Agent Plugins 1.0.0 | ❌ Per-client manifests |
| Hosting                                  | ✅ Remote (no local install) | ❌ Local stdio install |
| Tools                                    | ✅ 6 tools + 13 skills | ❌ 1 (transcript only) |
| YouTube search                           | ✅ Yes             | ❌ No |
| Channel & playlist extraction            | ✅ Yes             | ❌ No |
| Latest-uploads monitoring (free)         | ✅ Yes             | ❌ No |
| OAuth 2.1 + API key auth                 | ✅ Both            | ❌ Usually neither |
| Production scale (15M+ req/mo)           | ✅ Yes             | ❌ Hobbyist scrapers |
| Works on mobile Claude & web Claude      | ✅ Yes             | ❌ No |
| Agent-friendly error messages            | ✅ Yes             | ❌ Bare HTTP codes |
| No yt-dlp, no headless browser, no binaries | ✅ Just an API call | ❌ Blocked on cloud IPs |

---

## ⚡ Install

### As an Agent Plugin <sub>· **recommended**</sub>

Agent Plugins 1.0.0 standardizes the *package format*, not installation — so each client owns its own install flow. Point any of them at this repository:

```txt
https://github.com/ZeroPointRepo/transcriptapi-plugin
```

<details open>
<summary><b>VS Code</b></summary>

Command Palette → **Chat: Install Plugin From Source**, then paste the repo URL above.

Or register a local clone in `settings.json`:

```json
"chat.pluginLocations": { "/absolute/path/to/transcriptapi-plugin": true }
```

</details>

<details>
<summary><b>Cursor</b></summary>

**Customize** in the sidebar → find the plugin → **Install**. Or type `/add-plugin` and enter the repo URL.

For a local clone:

```bash
git clone https://github.com/ZeroPointRepo/transcriptapi-plugin ~/.cursor/plugins/local/transcriptapi
```

Then **Developer: Reload Window**.

</details>

<details>
<summary><b>Claude Code</b></summary>

```bash
/plugin marketplace add ZeroPointRepo/transcriptapi-plugin
/plugin install transcriptapi@transcriptapi
```

</details>

<details>
<summary><b>ChatGPT · Codex · GitHub Copilot · Kiro · others</b></summary>

Point your client's plugin mechanism at this repository, or at a local clone. The package carries the canonical `plugin.json` and `mcp.json`, plus per-client manifests under `.codex-plugin/`, `.cursor-plugin/` and `.claude-plugin/` for clients that look there first.

</details>

The first YouTube question you ask opens a TranscriptAPI OAuth sign-in (free account, 100 credits, no card). Done.

### Skills only (no MCP)

Every skill also works standalone against the REST API with an API key:

```bash
# All 13 skills
npx skills add ZeroPointRepo/transcriptapi-plugin

# Just the one you want — youtube-full covers everything
npx skills add ZeroPointRepo/transcriptapi-plugin --skill youtube-full
```

<details>
<summary><b>OpenClaw · Hermes · manual</b></summary>

**🦞 OpenClaw (ClawdBot/Moltbot):**
```bash
npx clawhub@latest install youtube-full
```

**Hermes Agent:**
```bash
hermes skills install skills-sh/ZeroPointRepo/transcriptapi-plugin/skills/youtube-full
```

**Manual:**
```bash
git clone https://github.com/ZeroPointRepo/transcriptapi-plugin.git
cp -r transcriptapi-plugin/skills/youtube-full ~/.claude/skills/
```

</details>

> **Not a developer?** Paste this into Claude, ChatGPT, OpenClaw or any agent:
>
> ```txt
> Install the TranscriptAPI plugin from https://github.com/ZeroPointRepo/transcriptapi-plugin
> I want YouTube transcripts, search and channel browsing from my agent. Set it up for me.
> ```

> **Tip — auto-invoke.** Add this rule to your client so you never have to ask explicitly:
>
> ```txt
> When I share a YouTube URL, automatically use TranscriptAPI to fetch the transcript
> before responding. This applies to any video analysis, summarization, or question
> about YouTube content.
> ```

<details>
<summary><b>Manual MCP configuration for 20+ other clients</b></summary>

The MCP endpoint is `https://transcriptapi.com/mcp`. Get an API key from your [dashboard](https://transcriptapi.com/dashboard/api-keys) if your client doesn't do OAuth.

**Claude Desktop & Web** — Settings → **Connectors** → **Add custom connector** → name `TranscriptAPI`, URL `https://transcriptapi.com/mcp` → **Connect**. [Full guide →](https://transcriptapi.com/docs/mcp/claude)

**Claude Code (CLI)**
```sh
claude mcp add --transport http transcript-api https://transcriptapi.com/mcp
```

**ChatGPT** — enable Developer Mode, then `Settings` → `Connected Apps` → `Add` → URL `https://transcriptapi.com/mcp`. Leave Client ID/Secret blank for Dynamic Client Registration. [Full guide →](https://transcriptapi.com/docs/mcp/chatgpt)

**OpenAI Agent Builder** — add an MCP Server tool, URL `https://transcriptapi.com/mcp`, auth **API Key**. [Guide →](https://transcriptapi.com/docs/mcp/openai-agent-builder)

**Amp**
```sh
amp mcp add transcript-api https://transcriptapi.com/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

**Cursor** (`~/.cursor/mcp.json`) · **LM Studio** · **BoltAI** · **JetBrains AI Assistant** · **Trae**
```json
{
  "mcpServers": {
    "transcript-api": {
      "url": "https://transcriptapi.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**VS Code** (`settings.json`) · **Roo Code** · **Kilo Code** (`.kilocode/mcp.json`)
```json
"mcp.servers": {
  "transcript-api": {
    "type": "http",
    "url": "https://transcriptapi.com/mcp",
    "headers": { "Authorization": "Bearer YOUR_API_KEY" }
  }
}
```

**Cline**
```json
{ "mcpServers": { "transcript-api": {
  "url": "https://transcriptapi.com/mcp", "type": "streamableHttp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" } } } }
```

**Windsurf** (`~/.codeium/windsurf/mcp_config.json`) · **Google Antigravity**
```json
{ "mcpServers": { "transcript-api": {
  "serverUrl": "https://transcriptapi.com/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" } } } }
```

**Zed** (`settings.json`)
```json
{ "context_servers": { "transcript-api": {
  "source": "remote", "url": "https://transcriptapi.com/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" } } } }
```

**Gemini CLI** (`~/.gemini/settings.json`) · **Qwen Coder** (`~/.qwen/settings.json`)
```json
{ "mcpServers": { "transcript-api": {
  "httpUrl": "https://transcriptapi.com/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" } } } }
```

**Augment Code** (`settings.json` under `augment.advanced`)
```json
"augment.advanced": { "mcpServers": [
  { "name": "transcript-api", "url": "https://transcriptapi.com/mcp",
    "headers": { "Authorization": "Bearer YOUR_API_KEY" } } ] }
```

**Warp** (Settings → AI → MCP) · **Perplexity Desktop** (Settings → Connectors → Advanced)
```json
{ "url": "https://transcriptapi.com/mcp",
  "headers": { "Authorization": "Bearer YOUR_API_KEY" } }
```

</details>

---

## 🛠️ The 6 MCP tools

All six are exposed automatically once you connect. **1 credit = 1 successful (HTTP 200) request.** Failed and rate-limited calls do not consume credits.

### 1. `get_youtube_transcript`

Fetch the transcript for any YouTube video — as markdown (with metadata) or structured JSON.

| Parameter           | Type    | Default      | Description                                    |
| ------------------- | ------- | ------------ | ---------------------------------------------- |
| `video_url`         | string  | **required** | YouTube URL (full or short) or 11-char video ID |
| `send_metadata`     | boolean | `true`       | Include video title, author, thumbnail         |
| `format`            | string  | `"text"`     | `"text"` (markdown) or `"json"`                |
| `include_timestamp` | boolean | `true`       | Add timestamps to each segment                 |

**Cost:** 1 credit.

<details>
<summary>Example output</summary>

Markdown:
```markdown
# Metadata

## Title: Rick Astley - Never Gonna Give You Up
## Author: RickAstleyVEVO

# Transcript

[0.0s] Never gonna give you up
[4.12s] Never gonna let you down
```

JSON:
```json
{
  "transcript": [
    { "text": "Never gonna give you up", "start": 0.0, "duration": 4.12 },
    { "text": "Never gonna let you down", "start": 4.12, "duration": 3.85 }
  ],
  "metadata": { "title": "Rick Astley...", "author_name": "RickAstleyVEVO" }
}
```

</details>

### 2. `search_youtube`

Search YouTube for videos or channels. Filter by type and paginate with a continuation token.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `query`        | string | **required** | Search query                         |
| `search_type`  | string | `"video"`    | `"video"` or `"channel"`             |
| `continuation` | string | `null`       | Token from a prior call for next page |

**Cost:** 1 credit per page (~20 results).

### 3. `get_channel_latest_videos` <sub>· **FREE**</sub>

The ~15 most recent uploads from any channel via RSS — no credits. Perfect for monitoring, daily recaps, or triggering downstream pipelines.

| Parameter | Type   | Default      | Description                                  |
| --------- | ------ | ------------ | -------------------------------------------- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` channel ID |

**Cost:** Free.

### 4. `search_channel_videos`

Search inside one specific channel for videos matching a query.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `channel`      | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `query`        | string | **required** | Query to search within the channel   |
| `continuation` | string | `null`       | Pagination token                     |

**Cost:** 1 credit per page (~30 results).

### 5. `list_channel_videos`

List every video on a channel, ~100 per page. Ideal for building databases or bulk transcript extraction.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `channel`      | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null`       | Pagination token                     |

**Cost:** 1 credit per page (~100 results).

### 6. `list_playlist_videos`

Every video in a YouTube playlist (PL/UU/LL/FL/OL IDs supported). Process entire courses or lecture series in a single call.

| Parameter      | Type   | Default      | Description                  |
| -------------- | ------ | ------------ | ---------------------------- |
| `playlist`     | string | **required** | Playlist URL or playlist ID  |
| `continuation` | string | `null`       | Pagination token             |

**Cost:** 1 credit per page (~100 results).

---

## 🎯 The 13 skills

`youtube` is the MCP-aware skill — it teaches the agent to drive the 6 tools above. `youtube-full` is the REST equivalent and the best pick if you installed skills without the MCP server. The rest are narrower variants and aliases, so the right skill fires however you phrase the request.

| Skill | What it does |
|-------|--------------|
| **youtube** | MCP-first — when and how to use each of the 6 hosted tools, and how not to waste credits |
| **youtube-full** | Complete REST toolkit — transcripts + search + channels + playlists |
| **transcript** | Extract a transcript from any YouTube video with timestamps |
| **captions** | Get closed captions / CC from YouTube videos |
| **subtitles** | Extract subtitles from YouTube videos |
| **video-transcript** | Convert YouTube videos to text transcripts |
| **youtube-search** | Search YouTube for videos and channels |
| **youtube-channels** | Browse channel uploads, get latest videos, resolve `@handles` |
| **youtube-playlist** | Fetch every video from a YouTube playlist |
| **youtube-data** | YouTube video and channel data — lightweight alternative to Google's API |
| **youtube-api** | YouTube API access for agents — no Google quota hassle |
| **transcriptapi** | Full TranscriptAPI access across all endpoints |
| **yt** | Quick YouTube utility for fast lookups |

---

## 💡 Use cases

| Use case                       | Example prompt                                                                                  |
| ------------------------------ | ----------------------------------------------------------------------------------------------- |
| 📝 **Summarize a video**       | "Summarize the key points from this video: [URL]"                                               |
| 🔍 **Research a topic**        | "Search YouTube for the 5 most-watched videos on neural radiance fields; summarize each."        |
| 🧠 **Study notes**             | "Create study notes from this MIT lecture series playlist: [PLAYLIST URL]"                       |
| ⚖️ **Compare perspectives**    | "Compare arguments in these two videos: [URL1] [URL2]"                                          |
| 🌐 **Translate**               | "Translate this video's transcript to Spanish: [URL]"                                           |
| ✍️ **Repurpose content**        | "Turn this video into a 1,500-word blog post: [URL]"                                            |
| 📡 **Monitor a creator**       | "Each morning, list new uploads from @hubermanlab and tell me which to watch."                  |
| 🏛️ **Build a content database** | "Pull every video from @veritasium and store title + transcript."                              |
| 🎯 **Competitor analysis**      | "Search inside @MKBHD for any video about [competitor product] and summarize the takeaways."   |

---

## 🔐 Authentication

**There are no credentials in this package.** Agent Plugins 1.0.0 has no portable field for embedding secrets, and authorization is client-managed.

### OAuth 2.1 <sub>· recommended</sub>

- **Dynamic Client Registration (DCR)** — Claude Desktop, Claude Web, ChatGPT and every Agent Plugins client. Just add the plugin; the client auto-registers and you authorize once via browser redirect. No key to copy.
- **Static registration** — optional on ChatGPT. Get Client ID + Secret from the [MCP Integration Dashboard](https://transcriptapi.com/dashboard/mcp-integration).

### API key

Universal fallback, and what the REST skills use.

1. Get your key from your [dashboard](https://transcriptapi.com/dashboard/api-keys) — keys start with `sk_`
2. Send it as a Bearer token: `"Authorization": "Bearer sk_your_api_key_here"`

For skills, export it once:

```bash
export TRANSCRIPT_API_KEY="sk_your_key_here"
```

> **Security:** store keys in environment variables and never commit them to version control. When you install a skill, most agents will offer to run the free signup + OTP flow and save the key for you automatically.

<details>
<summary><b>Where agents save the key</b></summary>

| Runtime | File |
|----------|------|
| **OpenClaw/Moltbot** | `~/.openclaw/openclaw.json` or `~/.clawdbot/moltbot.json` |
| **Hermes Agent** | Hermes secret store (`TRANSCRIPT_API_KEY`) |
| **macOS shell** | `~/.zshenv`, `~/.zprofile` |
| **Linux shell** | `~/.profile`, `~/.bashrc`, `~/.zshenv` |
| **Fish shell** | `~/.config/fish/config.fish` |
| **Fallback** | `~/.transcriptapi` (mode 600) |

</details>

---

## 💳 Pricing & rate limits

| Plan                | Price               | Credits      | Rate limit  |
| ------------------- | ------------------- | ------------ | ----------- |
| **Free**            | $0 (one-time)       | 100          | 60 req/min  |
| **Starter Monthly** | $5/month            | 1,000/month  | 200 req/min |
| **Starter Annual**  | $54/year ($4.50/mo) | 1,000/month  | 300 req/min |

- **1 credit** = 1 successful request (HTTP 200).
- Failed and rate-limited requests do **not** consume credits.
- `get_channel_latest_videos` is **free**.

[View pricing](https://transcriptapi.com/#pricing) · [Manage credits](https://transcriptapi.com/billing)

---

## 🚨 Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `401 Unauthorized` | Key missing, mistyped, or not loaded into the environment | Confirm the key starts with `sk_` and is set in the shell your agent runs in. If using OAuth, re-authorize. |
| `402 Payment Required` | Out of credits | Check your balance at [transcriptapi.com/billing](https://transcriptapi.com/billing) |
| `403` (Cloudflare `1010`) | Request sent without a User-Agent header | Send your agent's name as the User-Agent, e.g. `HermesAgent/0.11.0` |
| `404 Not Found` | Video has no captions, is private, age-restricted or region-locked | Verify the URL opens in a browser and the player shows captions |
| `408 Request Timeout` | Temporary upstream pressure | Transient — retry once after ~2s |
| `422 Validation Error` | Malformed channel or playlist reference | Channels accept `@handle`, a channel URL, or a `UC` ID; playlists accept `PL`, `UU`, `LL`, `FL`, `OL` |
| `429 Too Many Requests` | Rate limit reached | Wait and respect the `Retry-After` header |

Three more worth knowing:

- **Key saved but the agent can't see it.** Shell config files load per shell type — check the table above and make sure the file matches the shell your agent actually runs in. Restarting the agent after saving resolves most cases.
- **Live streams and premieres.** Transcripts appear after the stream ends and captions are processed, not while live.
- **Unexpected transcript language.** Many videos only carry captions in their original language. Request a preferred language, or ask your agent to translate the result.

<details>
<summary><b>OAuth issues</b></summary>

- Clear browser cookies and try again
- For ChatGPT, try switching between Dynamic and Static registration
- Ensure popup blockers aren't preventing the auth window

</details>

---

## 📁 Repo layout

```
transcriptapi-plugin/
├── plugin.json                 # Agent Plugins 1.0.0 manifest (canonical $schema)
├── mcp.json                    # hosted MCP server — streamable-http, OAuth, no keys
├── skills/                     # 13 skills, one per directory, each with SKILL.md
│   ├── youtube/                #   MCP-first — drives the 6 hosted tools
│   ├── youtube-full/           #   REST-first — the full toolkit
│   └── …                       #   transcript · captions · subtitles · search · channels · playlists …
├── assets/                     # black-background brand marks (SVG + PNG 64→1024)
├── server.json                 # MCP Registry descriptor
├── smithery.yaml · glama.json  # directory listings
├── marketplace.json            # marketplace index (single-plugin)
├── .claude-plugin/ .cursor-plugin/ .codex-plugin/ .plugin/
│                               # per-client discovery paths — same metadata, one per client
└── .github/workflows/          # CI: validates both manifests against the canonical schemas
```

The canonical package is `plugin.json` + `skills/` + `mcp.json`. Everything else is discovery convenience for clients that look elsewhere first.

---

## ✅ Verify this package

No secrets, no executable code, no `stdio` servers — nothing here runs on your machine. Check it yourself:

```bash
curl -sO https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
curl -sO https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
npx -y ajv-cli@5 validate --spec=draft2020 -s plugin.schema.json -d plugin.json
npx -y ajv-cli@5 validate --spec=draft2020 -s mcp.schema.json    -d mcp.json
```

Both print `valid`. CI runs exactly this on every push. See [SECURITY.md](SECURITY.md).

---

## 🔗 Also available as a REST API

Building an app instead of an agent? The same backend ships as a JSON REST API.

|                 | Agent Plugin / MCP          | REST API                                                  |
| --------------- | --------------------------- | --------------------------------------------------------- |
| **Best for**    | AI assistants & agents      | Apps & backend services                                   |
| **Setup**       | One install                 | Code integration                                          |
| **Get started** | This README                 | [API docs →](https://transcriptapi.com/docs/api) · [Swagger →](https://transcriptapi.com/swagger) |

Base URL: `https://transcriptapi.com/api/v2`

---

## 📋 MCP Registry

Published to the official [Model Context Protocol Registry](https://registry.modelcontextprotocol.io/) as:

```
com.transcriptapi/youtube-transcript-and-youtube-search
```

---

## 🔀 Related repos

- **Standalone MCP server:** [ZeroPointRepo/youtube-mcp](https://github.com/ZeroPointRepo/youtube-mcp)
- **Standalone agent skills (API-key based):** [ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills)
- **Verified Agent Plugins directory:** [ZeroPointRepo/awesome-agent-plugins](https://github.com/ZeroPointRepo/awesome-agent-plugins)

---

## 🤝 Connect

- 🌐 **Website:** [transcriptapi.com](https://transcriptapi.com)
- 📚 **Docs:** [transcriptapi.com/docs](https://transcriptapi.com/docs)
- 🔧 **API Reference:** [transcriptapi.com/docs/api](https://transcriptapi.com/docs/api)
- 🤖 **MCP setup guides:** [Claude](https://transcriptapi.com/docs/mcp/claude) · [ChatGPT](https://transcriptapi.com/docs/mcp/chatgpt) · [OpenAI Agent Builder](https://transcriptapi.com/docs/mcp/openai-agent-builder)
- 💬 **Contact:** [transcriptapi.com/contact](https://transcriptapi.com/contact)

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclosure

TranscriptAPI is an independent product and is not affiliated with, endorsed by, or sponsored by YouTube or Google.

---

<p align="center">
  <sub>© 2026 Zero Point Studio d.o.o. · Released under the <a href="./LICENSE">MIT License</a></sub>
</p>
