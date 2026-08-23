---
name: yt
description: "Use when YouTube is relevant: pasted video links or IDs, @handles, quick video lookups, summaries, channel latest uploads, topic search, or any request involving YouTube content — even if YouTube is not mentioned explicitly. Covers transcripts, search, and channel latest. Not for uploads or account management."
license: MIT
compatibility: "Requires internet access to reach transcriptapi.com. No additional runtimes or dependencies needed."
metadata:
  version: "1.5.0"
  publisher: "Zero Point Studio"
  homepage: "https://transcriptapi.com"
  user-invocable: "true"
  requires-env: "TRANSCRIPT_API_KEY"
  env-prompt: "Your TranscriptAPI key (starts with sk_)"
  env-help: "Free account at https://transcriptapi.com - 100 credits, no card required. Or let the agent create one for you."
  openclaw-emoji: "▶️"
  openclaw-primary-env: "TRANSCRIPT_API_KEY"
  hermes-category: "media"
  hermes-tags: "youtube, transcripts, video, search, channels, playlists"
---

# yt

Quick YouTube lookup via [TranscriptAPI.com](https://transcriptapi.com).

## Setup

If `$TRANSCRIPT_API_KEY` is not set, read [references/auth-setup.md](references/auth-setup.md) and follow the instructions there to get and store the key.

## Required Headers

Every request needs two headers:

- **Authorization:** `Bearer $TRANSCRIPT_API_KEY`
- **User-Agent:** your agent's name and version if known (e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0`). Version is optional — agent name alone is fine. Do not omit this header or send a bare default — Cloudflare will return a 403 (error code 1010) and block the request.

## API Reference

Full OpenAPI spec: [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — consult this for the latest parameters and schemas.

## Transcript — 1 credit

```http
GET https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

## Search — 1 credit

```http
GET https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=10
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

| Param   | Default | Values                 |
| ------- | ------- | ---------------------- |
| `q`     | —       | 1-200 chars (required) |
| `type`  | `video` | `video`, `channel`     |
| `limit` | `20`    | 1-50                   |

## Channel latest — FREE

```http
GET https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

Returns last 15 videos with exact view counts and publish dates. Accepts `@handle`, channel URL, or `UC...` ID.

## Resolve handle — FREE

```http
GET https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED
Authorization: Bearer $TRANSCRIPT_API_KEY
User-Agent: YourAgent/1.0
```

Use to convert @handle to UC... channel ID.

## Errors

| Code     | Meaning          | Action                                         |
| -------- | ---------------- | ---------------------------------------------- |
| 401      | Bad API key      | Check key                                      |
| 402      | No credits       | transcriptapi.com/billing                      |
| 403/1010 | Cloudflare block | Add or fix User-Agent header                   |
| 404      | Not found        | No captions or resource doesn't exist          |
| 408      | Timeout          | Retry once                                     |

Free tier: 100 credits. Search and transcript cost 1 credit. Channel latest and resolve are free.

## Copy-paste examples

Every request in this file as a ready-to-run one-liner: [references/curl-examples.md](references/curl-examples.md)
