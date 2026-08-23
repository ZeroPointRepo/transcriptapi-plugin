# REST API reference — fallback path

Use this only when the `transcriptapi` MCP tools are **not** available. Same backend, same
credit costs.

Base URL: `https://transcriptapi.com/api/v2`
Live OpenAPI spec: <https://transcriptapi.com/openapi.json>

## Required headers on every request

| Header | Value |
| --- | --- |
| `Authorization` | `Bearer $TRANSCRIPT_API_KEY` |
| `User-Agent` | Your agent's name, optionally with a version — e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0` |

> **Do not omit `User-Agent` or send a bare default.** Cloudflare returns a 403 with error
> code 1010 and blocks the request. Agent name alone is fine; the version is optional.

If `$TRANSCRIPT_API_KEY` is not set, follow [auth-setup.md](auth-setup.md).

---

## Transcript — 1 credit

```http
GET /youtube/transcript?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `video_url` | yes | — | YouTube URL or 11-character video ID |
| `format` | no | `json` | `json`, `text` |
| `include_timestamp` | no | `true` | `true`, `false` |
| `send_metadata` | no | `false` | `true`, `false` |

Note the REST defaults differ from the MCP tool's: pass
`format=text&include_timestamp=true&send_metadata=true` explicitly unless the user asked
otherwise.

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [{ "text": "...", "start": 18.0, "duration": 3.5 }],
  "metadata": { "title": "...", "author_name": "...", "author_url": "..." }
}
```

```bash
curl -sG https://transcriptapi.com/api/v2/youtube/transcript \
  --data-urlencode "video_url=https://youtu.be/dQw4w9WgXcQ" \
  -d format=text -d include_timestamp=true -d send_metadata=true \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

---

## Search — 1 credit

```http
GET /youtube/search?q=QUERY&type=video&limit=20
```

| Param | Required | Default | Validation |
| --- | --- | --- | --- |
| `q` | yes | — | 1–200 characters |
| `type` | no | `video` | `video`, `channel` |
| `limit` | no | `20` | 1–50 |

---

## Channels

Every channel endpoint accepts `channel` as an `@handle`, a channel URL, or a `UC…` ID. There
is no need to resolve first.

### Resolve a handle — FREE

```http
GET /youtube/channel/resolve?input=@TED
```

```json
{ "channel_id": "UC...", "resolved_from": "@TED" }
```

### Latest ~15 videos — FREE

```http
GET /youtube/channel/latest?channel=@TED
```

Returns exact `viewCount` and ISO `published` timestamps.

### All channel videos — 1 credit per page

```http
GET /youtube/channel/videos?channel=@NASA          # first page, ~100 videos
GET /youtube/channel/videos?continuation=TOKEN     # subsequent pages
```

Provide **exactly one** of `channel` or `continuation`. The response carries
`continuation_token` and `has_more`.

### Search within a channel — 1 credit

```http
GET /youtube/channel/search?channel=@TED&q=QUERY&limit=30
```

---

## Playlists — 1 credit per page

```http
GET /youtube/playlist/videos?playlist=PL_ID        # first page
GET /youtube/playlist/videos?continuation=TOKEN    # subsequent pages
```

Valid ID prefixes: `PL`, `UU`, `LL`, `FL`, `OL`. Response includes `playlist_info`, `results`,
`continuation_token` and `has_more`.

---

## Credit costs

| Endpoint | Cost |
| --- | --- |
| `/youtube/transcript` | 1 |
| `/youtube/search` | 1 |
| `/youtube/channel/resolve` | **free** |
| `/youtube/channel/latest` | **free** |
| `/youtube/channel/videos` | 1 / page |
| `/youtube/channel/search` | 1 |
| `/youtube/playlist/videos` | 1 / page |

## Validation rules

| Field | Rule |
| --- | --- |
| `video_url` | YouTube URL (full, `youtu.be`, or shorts) or 11-character ID |
| `channel` | `@handle`, channel URL, or `UC…` ID |
| `playlist` | Playlist URL or ID with a `PL`/`UU`/`LL`/`FL`/`OL` prefix |
| `q` | 1–200 characters |
| `limit` | 1–50 |

## Worked example — research workflow

```bash
# 1. find candidates
curl -sG https://transcriptapi.com/api/v2/youtube/search \
  --data-urlencode "q=machine learning explained" -d limit=5 \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"

# 2. transcribe only the ones worth reading
curl -sG https://transcriptapi.com/api/v2/youtube/transcript \
  --data-urlencode "video_url=VIDEO_ID" \
  -d format=text -d include_timestamp=true -d send_metadata=true \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"
```
