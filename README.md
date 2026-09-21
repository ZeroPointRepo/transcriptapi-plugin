<!-- mcp-name: com.transcriptapi/youtube-transcript-and-youtube-search -->

<p align="center">
  <a href="https://transcriptapi.com">
    <img src="assets/logo-512.png" width="160" height="160" alt="TranscriptAPI" />
  </a>
</p>

<h1 align="center">YouTube MCP + YouTube Skill for AI Agents</h1>

<p align="center">
  <b>The complete YouTube toolkit as a single Agent Plugin, by <a href="https://transcriptapi.com">TranscriptAPI</a>.</b><br/>
  YouTube transcripts, video &amp; channel metadata, captions and subtitles, video &amp; channel search, channel browsing, playlist extraction and new-upload polling: 12 hosted MCP tools plus one skill.<br/>
  One install. OAuth sign-in. No API key to manage. Free tier, no card.
</p>

<p align="center">
  <a href="https://agent-plugins.org/specification"><img src="https://img.shields.io/badge/Agent_Plugins-1.0.0-6E56CF?style=for-the-badge" alt="Agent Plugins 1.0.0"/></a>
  <a href="https://github.com/ZeroPointRepo/transcriptapi-plugin/actions/workflows/validate-plugin.yml"><img src="https://img.shields.io/github/actions/workflow/status/ZeroPointRepo/transcriptapi-plugin/validate-plugin.yml?style=for-the-badge&label=spec%20valid" alt="Spec conformance"/></a>
  <a href="https://transcriptapi.com/docs"><img src="https://img.shields.io/badge/Docs-transcriptapi.com-06B6D4?style=for-the-badge" alt="Docs"/></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge" alt="MIT License"/></a>
</p>

> **Powering 15M+ transcripts every month** · 500K+ transcripts processed daily · 49ms median response time
> Trusted in production by [youtubetotranscript.com](https://youtubetotranscript.com) (~11M/mo) and [recapio.com](https://recapio.com) (~2.8M/mo).

---

## 🧩 What is this?

This repository root is a conformant **[Agent Plugins 1.0.0](https://agent-plugins.org/specification)** package: the open, vendor-neutral packaging standard published 2026-08-06 by Amazon, Cursor, GitHub, Microsoft, OpenAI and Vercel, with Google as a core maintainer. It bundles **MCP servers and Agent Skills** into one portable, drop-in folder that every compliant client can read.

One install gives your agent both halves:

| Component | What it does |
|---|---|
| **MCP server** (`transcriptapi`) | 12 hosted tools over streamable HTTP with OAuth 2.1: `get_youtube_transcript`, `get_youtube_video_info`, `get_video_metadata`, `search_youtube`, `get_channel_info`, `get_channel_latest_videos`, `search_channel_videos`, `list_channel_videos`, `list_channel_playlists`, `list_channel_posts`, `get_channel_sections`, `list_playlist_videos`. No key handling: your agent signs you in on first use. |
| **Skill** (`youtube`) | Teaches the agent *when* to reach for YouTube data, which tool answers each question, and how not to burn credits, with a full REST fallback for clients that load skills but not MCP servers. |

**Just ask, in plain English:**

```txt
Summarize this video for me: https://youtu.be/UF8uR6Z6KLc
Find @NASA's three most-viewed videos about the Moon landing and compare them.
What has @TED posted in the last month?
```

That last set of prompts touches 3 of the 12 tools (`search_youtube`, `search_channel_videos`, `get_youtube_transcript`) without you writing a line of code.

---

## Why TranscriptAPI

Most YouTube integrations do one thing: pull a single transcript. **This is a full toolkit.**

|                                          | TranscriptAPI | Typical YouTube MCP / skill |
| ---------------------------------------- | ----------------- | ------------------- |
| Packaging                                | ✅ Agent Plugins 1.0.0 | ❌ Per-client manifests |
| Hosting                                  | ✅ Remote (no local install) | ❌ Local stdio install |
| Tools                                    | ✅ 12 tools + a skill | ❌ 1 (transcript only) |
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

Agent Plugins 1.0.0 standardizes the *package format*, not installation, so each client owns its own install flow. Point any of them at this repository:

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

The skill also works standalone against the REST API with an API key:

```bash
npx skills add ZeroPointRepo/transcriptapi-plugin
```

<details>
<summary><b>OpenClaw · Hermes · manual</b></summary>

**🦞 OpenClaw (ClawdBot/Moltbot):** installs from the ClawHub registry, which serves the standalone skills repo:
```bash
npx clawhub@latest install youtube-full
```

**Hermes Agent:**
```bash
hermes skills install skills-sh/ZeroPointRepo/transcriptapi-plugin/skills/youtube
```

**Manual:**
```bash
git clone https://github.com/ZeroPointRepo/transcriptapi-plugin.git
cp -r transcriptapi-plugin/skills/youtube ~/.claude/skills/
```

</details>

> **Not a developer?** Paste this into Claude, ChatGPT, OpenClaw or any agent:
>
> ```txt
> Install the TranscriptAPI plugin from https://github.com/ZeroPointRepo/transcriptapi-plugin
> I want YouTube transcripts, search and channel browsing from my agent. Set it up for me.
> ```

> **Tip: auto-invoke.** Add this rule to your client so you never have to ask explicitly:
>
> ```txt
> When I share a YouTube URL, automatically use TranscriptAPI to fetch the transcript
> before responding. This applies to any video analysis, summarization, or question
> about YouTube content.
> ```

<details>
<summary><b>Manual MCP configuration for 20+ other clients</b></summary>

The MCP endpoint is `https://transcriptapi.com/mcp`. Get an API key from your [dashboard](https://transcriptapi.com/dashboard/api-keys) if your client doesn't do OAuth.

One-click, if you'd rather skip the config. Note these add the **MCP server only**, not the bundled skill:

<a href="https://cursor.com/en/install-mcp?name=transcript-api&config=eyJ1cmwiOiJodHRwczovL3RyYW5zY3JpcHRhcGkuY29tL21jcCJ9"><img alt="Add to Cursor" src="https://img.shields.io/badge/Cursor-Add_MCP-000000?style=flat-square&logo=cursor&logoColor=white"/></a>
<a href="https://insiders.vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22transcript-api%22%2C%22url%22%3A%22https%3A%2F%2Ftranscriptapi.com%2Fmcp%22%7D"><img alt="Add to VS Code" src="https://img.shields.io/badge/VS_Code-Add_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white"/></a>

**Claude Desktop & Web**: Settings → **Connectors** → **Add custom connector** → name `TranscriptAPI`, URL `https://transcriptapi.com/mcp` → **Connect**. [Full guide →](https://transcriptapi.com/docs/mcp/claude)

**Claude Code (CLI)**
```sh
claude mcp add --transport http transcript-api https://transcriptapi.com/mcp
```

**ChatGPT**: enable Developer Mode, then `Settings` → `Connected Apps` → `Add` → URL `https://transcriptapi.com/mcp`. Leave Client ID/Secret blank for Dynamic Client Registration. [Full guide →](https://transcriptapi.com/docs/mcp/chatgpt)

**OpenAI Agent Builder**: add an MCP Server tool, URL `https://transcriptapi.com/mcp`, auth **API Key**. [Guide →](https://transcriptapi.com/docs/mcp/openai-agent-builder)

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

## 🛠️ The 12 MCP tools

All 12 are exposed automatically once you connect. **Successful calls cost 1 credit unless a tool states otherwise below.** Failed and rate-limited calls do not consume credits.

> **Which video tool?** Use `get_youtube_video_info` (free) to discover transcript languages before fetching a transcript. Use `get_video_metadata` (1 credit) for view/like counts, publish date, description, duration, tags, or related videos.

### 1. `get_youtube_transcript`

Fetch the transcript for any YouTube video, as markdown (with metadata) or structured JSON.

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

### 2. `get_youtube_video_info` <sub>· **FREE**</sub>

Basic metadata (title, author, thumbnail) plus the available transcript languages: call before `get_youtube_transcript` to pick a language.

| Parameter   | Type   | Default      | Description                                     |
| ----------- | ------ | ------------ | ------------------------------------------------ |
| `video_url` | string | **required** | YouTube URL (full or short) or 11-char video ID |

**Cost:** Free.

### 3. `get_video_metadata`

Rich video metadata without needing captions: view/like-count text, publish date, structured description, channel summary, thumbnails. Optional `include` extras add duration/category/tags/caption tracks and related videos.

| Parameter   | Type     | Default | Description                                                                                |
| ----------- | -------- | ------- | -------------------------------------------------------------------------------------------- |
| `video_url` | string   | **required** | YouTube URL (full or short) or 11-char video ID                                        |
| `include`   | string[] | _none_  | `"details"` (duration, category, tags, caption tracks) and/or `"related"` (related videos)     |

**Cost:** 1 credit.

### 4. `search_youtube`

Search YouTube for videos, channels, playlists, or movies. Filter by type, sort, upload date or duration, and paginate with a continuation token.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `query`        | string | **required** (first call) | Search query            |
| `search_type`  | string | `"video"`    | `"video"`, `"channel"`, `"playlist"`, or `"movie"` (first call only) |
| `sort`         | string | `"relevance"` | `"relevance"` or `"views"` (first call only) |
| `upload_date`  | string | _none_       | `hour`, `today`, `week`, `month`, `year` (first call, videos only) |
| `duration`     | string | _none_       | `short`, `medium`, `long` (first call, videos only) |
| `continuation` | string | `null`       | Token from a prior call for next page |

**Cost:** 1 credit per page (~20 results).

### 5. `get_channel_info`

A channel's profile: title, `@handle`, verified flag, subscriber/video-count text, description, keywords, tags, thumbnails, banners, and the tabs it exposes.

| Parameter | Type   | Default      | Description                                  |
| --------- | ------ | ------------ | --------------------------------------------- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` channel ID |

**Cost:** 1 credit.

### 6. `get_channel_latest_videos` <sub>· **FREE**</sub>

The ~15 most recent uploads from any channel via RSS. Perfect for monitoring, daily recaps, or triggering downstream pipelines.

| Parameter | Type   | Default      | Description                                  |
| --------- | ------ | ------------ | -------------------------------------------- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` channel ID |

**Cost:** Free.

### 7. `search_channel_videos`

Search inside one specific channel for videos matching a query.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `channel`      | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `query`        | string | **required** | Query to search within the channel   |
| `continuation` | string | `null`       | Pagination token                     |

**Cost:** 1 credit per page (~30 results).

### 8. `list_channel_videos`

List a channel's feed, paginated. Use `tab` to choose the uploads feed (default, ~100/page), Shorts, or live streams (~48/page), and the optional `sort` to order the Videos tab by latest, popular, or oldest. Ideal for building databases or bulk transcript extraction.

| Parameter      | Type   | Default      | Description                          |
| -------------- | ------ | ------------ | ------------------------------------ |
| `channel`      | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `tab`          | string | `"videos"`   | `videos` (uploads), `shorts`, or `streams`. Repeat the same `tab` when paginating. |
| `sort`         | string | `null`       | `latest`, `popular`, or `oldest`. Omit for the uploads feed. Repeat the same value when paginating. |
| `continuation` | string | `null`       | Pagination token                     |

**Sorting.** Add sort=latest, popular, or oldest to channel/videos to get a channel's videos in the order you want, for example its most-popular uploads first. A sorted page returns about 30 videos (an unsorted page returns about 100), and every page costs the same 1 credit.

When paging, send the same sort on each request.

Every item carries **`members_only`**: `true` only when YouTube badges the video "Members only", and those items have no `viewCountText`. It is always `false` on the uploads feed, on `tab: "shorts"`, and on playlists.

Items from `tab: "streams"` carry `lengthText` and `publishedTimeText` (for example `Streamed 2 years ago`, or `LIVE` and a watching count while live). `tab: "shorts"` returns `null` for both, because YouTube's Shorts grid publishes neither. On the channel-tab feeds, `channelId`, `channelTitle`, `channelHandle` and `index` are `null`.

**Cost:** 1 credit per page.

### 9. `list_channel_playlists`

Paginated list of the playlists on a channel (id, title, URL, video-count text, thumbnails).

| Parameter      | Type   | Default | Description                          |
| -------------- | ------ | ------- | ------------------------------------ |
| `channel`      | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null`  | Pagination token                     |

**Cost:** 1 credit per page.

### 10. `list_channel_posts`

Paginated list of a channel's community (Posts tab) content: text, publish time, like-count text, and attachments. Channels without a community tab return an empty results list, not an error.

| Parameter      | Type   | Default | Description                          |
| -------------- | ------ | ------- | ------------------------------------ |
| `channel`      | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null`  | Pagination token                     |

**Cost:** 1 credit per page.

### 11. `get_channel_sections`

The curated, grouped sections of a channel page: titled shelves of videos, playlists, shorts, or featured channels, in the channel's own order.

| Parameter | Type   | Default      | Description                                                     |
| --------- | ------ | ------------ | ---------------------------------------------------------------- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `tab`     | string | `"featured"` | `featured` (Home), `podcasts`, or `releases` |

**Cost:** 1 credit.

### 12. `list_playlist_videos`

Every video in a YouTube playlist (PL/UU/LL/FL/OL IDs supported). Process entire courses or lecture series in a single call.

| Parameter      | Type   | Default      | Description                  |
| -------------- | ------ | ------------ | ---------------------------- |
| `playlist`     | string | **required** | Playlist URL or playlist ID  |
| `continuation` | string | `null`       | Pagination token             |

**Cost:** 1 credit per page (~100 results).

---

## 🎯 The `youtube` skill

One skill covers everything. It teaches the agent *when* YouTube is the right source, which tool answers each kind of question, and how not to burn credits: the judgement the MCP tool definitions can't carry on their own.

It handles both data paths automatically:

- **MCP available** → drives the 12 hosted tools above. OAuth, no key.
- **MCP not available** → falls back to the REST API with a `TRANSCRIPT_API_KEY`, so the skill still works in clients that load skills but not MCP servers.

Structured for [progressive disclosure](https://agentskills.io/specification#progressive-disclosure), so the agent pays for detail only when it needs it:

```
skills/youtube/
├── SKILL.md                    # routing, credit discipline, workflows (~130 lines)
└── references/
    ├── mcp-tools.md            # full parameter reference for the 12 tools
    ├── rest-api.md             # REST fallback: endpoints, curl, validation rules
    ├── auth-setup.md           # getting and persisting an API key
    └── errors.md               # error codes, retry policy, false alarms
```

Only `name` + `description` (~100 tokens) load at startup. The body loads when the skill activates; the references load only when actually consulted.

> **Looking for the granular skills?** v1.0.0 shipped 13 overlapping skills (`transcript`, `captions`, `subtitles`, `yt`, …). They were alias variants of one another, and thirteen near-identical descriptions competing at startup made skill selection *worse*, not better. They're consolidated here. The standalone, API-key-based versions still live in [ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills).

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
| 📡 **Monitor a creator**       | "Each morning, list new uploads from @TED and tell me which to watch."                  |
| 🏛️ **Build a content database** | "Pull every video from @NASA and store title + transcript."                              |
| 🎯 **Competitor analysis**      | "Search inside @NASA for any video about [a specific mission or topic] and summarize the takeaways."   |

---

## 🔐 Authentication

**There are no credentials in this package.** Agent Plugins 1.0.0 has no portable field for embedding secrets, and authorization is client-managed.

### OAuth 2.1 <sub>· recommended</sub>

- **Dynamic Client Registration (DCR)**: Claude Desktop, Claude Web, ChatGPT and every Agent Plugins client. Just add the plugin; the client auto-registers and you authorize once via browser redirect. No key to copy.
- **Static registration**: optional on ChatGPT. Get Client ID + Secret from the [MCP Integration Dashboard](https://transcriptapi.com/dashboard/mcp-integration).

### API key

Universal fallback, and what the REST skills use.

1. Get your key from your [dashboard](https://transcriptapi.com/dashboard/api-keys). Keys start with `sk_`
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
| `408 Request Timeout` | Temporary upstream pressure | Transient: retry once after ~2s |
| `422 Validation Error` | Malformed channel or playlist reference | Channels accept `@handle`, a channel URL, or a `UC` ID; playlists accept `PL`, `UU`, `LL`, `FL`, `OL` |
| `429 Too Many Requests` | Rate limit reached | Wait and respect the `Retry-After` header |

Three more worth knowing:

- **Key saved but the agent can't see it.** Shell config files load per shell type. Check the table above and make sure the file matches the shell your agent actually runs in. Restarting the agent after saving resolves most cases.
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
├── mcp.json                    # hosted MCP server: streamable-http, OAuth, no keys
├── skills/
│   └── youtube/                # one skill: SKILL.md + references/ (progressive disclosure)
├── assets/                     # black-background brand marks (SVG + PNG 64→1024)
├── server.json                 # MCP Registry descriptor
├── smithery.yaml · glama.json  # directory listings
├── marketplace.json            # marketplace index (single-plugin)
├── .claude-plugin/ .cursor-plugin/ .codex-plugin/ .plugin/
│                               # per-client discovery paths: same metadata, one per client
└── .github/workflows/          # CI: validates both manifests against the canonical schemas
```

The canonical package is `plugin.json` + `skills/` + `mcp.json`. Everything else is discovery convenience for clients that look elsewhere first.

---

## ✅ Verify this package

No secrets, no executable code, no `stdio` servers: nothing here runs on your machine. Check it yourself.

**1. Manifests against the canonical schemas:**

```bash
curl -sO https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
curl -sO https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
npx -y ajv-cli@5 validate --spec=draft2020 -s plugin.schema.json -d plugin.json
npx -y ajv-cli@5 validate --spec=draft2020 -s mcp.schema.json    -d mcp.json
```

**2. Every skill against the Agent Skills specification.** This is the check that actually matters: §7.1 requires skills to conform, and a conformant client **silently skips** any skill that doesn't. A plugin can have perfect manifests and still ship skills that never load.

```bash
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
for d in skills/*/; do skills-ref validate "$d"; done
```

It prints `Valid skill`.

**3. The normative requirements a schema can't express**: path safety, discovery depth, reverse-domain extension namespaces, transport rules:

```bash
python .github/scripts/check_conformance.py
```

CI runs the skill validation and the conformance checker on every pull request. The `ajv` step above is the canonical schema check. `check_conformance.py` enforces the same rules plus the ones a schema can't express, so running it locally is equivalent. See [SECURITY.md](SECURITY.md).

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

PRs welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclosure

TranscriptAPI is an independent product and is not affiliated with, endorsed by, or sponsored by YouTube or Google.

---

<p align="center">
  <sub>© 2026 TranscriptAPI · Released under the <a href="./LICENSE">MIT License</a></sub>
</p>
