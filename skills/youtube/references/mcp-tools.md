# MCP tool reference

The six tools exposed by the bundled `transcriptapi` MCP server
(`https://transcriptapi.com/mcp`, streamable HTTP, OAuth 2.1).

Authorization is handled by the client. There is no key to pass and no auth argument on any
tool. 1 credit = 1 successful call; failures and rate limits are never charged.

---

## `get_youtube_transcript`: 1 credit

Fetch the spoken content of a video. This is also the captions/subtitles path: same data.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `video_url` | string | **required** | Full URL, `youtu.be` short URL, shorts URL, or a bare 11-character video ID |
| `format` | string | `"text"` | `"text"` for markdown, `"json"` for per-segment objects |
| `include_timestamp` | boolean | `true` | Prefix each segment with its timestamp |
| `send_metadata` | boolean | `true` | Include title, author and thumbnail |

Use `format="json"` only when you need exact `start`/`duration` values to cite or seek to a
moment. `"text"` is cheaper to reason over.

**`format="text"`**

```markdown
# Metadata

## Title: Rick Astley - Never Gonna Give You Up
## Author: RickAstleyVEVO

# Transcript

[0.0s] Never gonna give you up
[4.12s] Never gonna let you down
```

**`format="json"`**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "Never gonna give you up", "start": 0.0, "duration": 4.12 },
    { "text": "Never gonna let you down", "start": 4.12, "duration": 3.85 }
  ],
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "author_name": "RickAstleyVEVO",
    "author_url": "https://www.youtube.com/@RickAstley",
    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

---

## `search_youtube`: 1 credit per page

Search YouTube for videos or channels. ~20 results per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `query` | string | **required** | 1-200 characters |
| `search_type` | string | `"video"` | `"video"` or `"channel"` |
| `continuation` | string | `null` | Token from a prior call, for the next page |

Returns metadata only, no transcripts. Pick the best hits, then transcribe those.

---

## `get_channel_latest_videos`: FREE

The ~15 most recent uploads from a channel, via RSS.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |

Costs nothing. Use it freely for anything about recent uploads, monitoring, or daily recaps.
Returns exact view counts and ISO publish timestamps.

---

## `search_channel_videos`: 1 credit per page

Search within a single channel. ~30 results per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `query` | string | **required** | Query to match inside that channel |
| `continuation` | string | `null` | Pagination token |

Always better than listing a whole channel and filtering client-side.

---

## `list_channel_videos`: 1 credit per page

A channel's full upload history, ~100 per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null` | Pagination token |

Only when the user genuinely wants the whole catalogue. For recent uploads use
`get_channel_latest_videos` (free); to find something specific use `search_channel_videos`.

---

## `list_playlist_videos`: 1 credit per page

Every video in a playlist, ~100 per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `playlist` | string | **required** | Playlist URL or ID: `PL`, `UU`, `LL`, `FL`, `OL` prefixes |
| `continuation` | string | `null` | Pagination token |

Confirm before transcribing a large playlist: that is one credit per video.
