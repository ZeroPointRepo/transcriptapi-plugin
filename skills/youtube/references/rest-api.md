# REST API reference: fallback path

Use this only when the `transcriptapi` MCP tools are **not** available. Same backend, same
credit costs.

Base URL: `https://transcriptapi.com/api/v2`
Live OpenAPI spec: <https://transcriptapi.com/openapi.json>

## Required headers on every request

| Header | Value |
| --- | --- |
| `Authorization` | `Bearer $TRANSCRIPT_API_KEY` |
| `User-Agent` | Your agent's name, optionally with a version, e.g. `HermesAgent/0.11.0`, `ClaudeCode/1.0` |

> **Do not omit `User-Agent` or send a bare default.** Cloudflare returns a 403 with error
> code 1010 and blocks the request. Agent name alone is fine; the version is optional.

If `$TRANSCRIPT_API_KEY` is not set, follow [auth-setup.md](auth-setup.md).

---

## Transcript: 1 credit

```http
GET /youtube/transcript?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `video_url` | yes | - | YouTube URL or 11-character video ID |
| `format` | no | `json` | `json`, `text` |
| `include_timestamp` | no | `true` | `true`, `false` |
| `send_metadata` | no | `false` | `true`, `false` |
| `language` | no | - | Priority list of transcript language codes |

Note the REST defaults differ from the MCP tool's: pass
`format=text&include_timestamp=true&send_metadata=true` explicitly unless the user asked
otherwise.

```json
{
  "video_id": "UF8uR6Z6KLc",
  "language": "en",
  "transcript": [{ "text": "...", "start": 18.0, "duration": 3.5 }],
  "metadata": { "title": "...", "author_name": "...", "author_url": "..." }
}
```

```bash
curl -sG https://transcriptapi.com/api/v2/youtube/transcript \
  --data-urlencode "video_url=https://youtu.be/UF8uR6Z6KLc" \
  -d format=text -d include_timestamp=true -d send_metadata=true \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" \
  -H "User-Agent: YourAgent/1.0"
```

---

## Video info: FREE

```http
GET /youtube/info?video_url=VIDEO_URL
```

Basic metadata (title, author, thumbnail) plus the video's available transcript languages:
call this **before** `/youtube/transcript` to pick a language. No credit used (still requires
an active plan). Returns `404` when the video does not exist or has no captions.

```json
{
  "video_id": "UF8uR6Z6KLc",
  "metadata": { "title": "...", "author_name": "...", "author_url": "...", "thumbnail_url": "..." },
  "available_languages": [
    { "code": "en", "name": "English" },
    { "code": "asr-en", "name": "English (auto-generated)" }
  ]
}
```

Each `available_languages[].code` can be passed to `/youtube/transcript`'s `language` param.
For counts, publish date, description, duration, tags, or related videos, use
`/youtube/video/metadata` instead.

---

## Video metadata: 1 credit

```http
GET /youtube/video/metadata?video_url=VIDEO_URL&include=details,related
```

> **Naming:** this endpoint was previously `/youtube/video/info`. That path still works as a
> hidden, deprecated alias: always call `/youtube/video/metadata` in new code.

Rich video metadata without needing captions: title, view/like-count text, publish date, a
structured description with extracted links, an uploading-channel summary, and thumbnails.

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `video_url` | yes | - | YouTube URL or 11-character video ID |
| `include` | no | - | Comma-separated: `details`, `related` |

`include=details` adds a `details` object (`lengthSeconds`, `category`, `tags`, caption-track
inventory) sourced from YouTube's player endpoint; when it can't be read, `details.available`
is `false` with a `reason` instead of a guessed value. `include=related` adds a `related` list
of suggested videos. Hidden counts are `null`, never `0`. Cached 5 minutes.

```bash
curl -sG https://transcriptapi.com/api/v2/youtube/video/metadata \
  --data-urlencode "video_url=UF8uR6Z6KLc" -d include=details,related \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"
```

---

## Search: 1 credit per page

```http
GET /youtube/search?q=QUERY&type=video
GET /youtube/search?continuation=TOKEN     # subsequent pages
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `q` | conditional | - | 1-200 characters. Required for the first page. |
| `type` | no | `video` | `video`, `channel`, `playlist`, `movie` (first page only) |
| `sort` | no | `relevance` | `relevance`, `views` (first page only) |
| `upload_date` | no | - | `hour`, `today`, `week`, `month`, `year` (first page, videos only) |
| `duration` | no | - | `short` (under 4m), `medium` (4-20m), `long` (over 20m) (first page, videos only) |
| `features` | no | - | Comma-separated: `hd`, `subtitles`, `cc`, `live`, `4k`, `hdr`, `360`, `creative_commons` (first page only) |
| `continuation` | conditional | - | Token from a prior call, for the next page |

Provide exactly one of `q` or `continuation`. Filters (`sort`, `upload_date`, `duration`,
`features`) apply to the first page only: the `continuation` token already encodes them.
~20 results per page.

```bash
curl -sG https://transcriptapi.com/api/v2/youtube/search \
  --data-urlencode "q=machine learning explained" -d type=video -d sort=views -d duration=long \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"
```

---

## Channels

Every channel endpoint accepts `channel` as an `@handle`, a channel URL, or a `UC…` ID. There
is no need to resolve first.

### Resolve a handle: FREE

```http
GET /youtube/channel/resolve?input=@TED
```

```json
{ "channel_id": "UC...", "resolved_from": "@TED" }
```

### Channel info: 1 credit

```http
GET /youtube/channel/info?channel=@TED
```

Profile: title, `@handle`, verified flag, subscriber/video-count text, description, keywords,
tags, thumbnails, banners, and `availableTabs`. Not paginated. Check `availableTabs` before
calling `/youtube/channel/sections` or `/youtube/channel/videos` with a `tab`.

### Latest ~15 videos: FREE

```http
GET /youtube/channel/latest?channel=@TED
```

Returns exact `viewCount` and ISO `published` timestamps.

### Channel videos (paginated): 1 credit per page

```http
GET /youtube/channel/videos?channel=@NASA               # first page, ~100 videos
GET /youtube/channel/videos?channel=@NASA&tab=shorts
GET /youtube/channel/videos?channel=@NASA&sort=popular  # Videos tab, most-viewed first, ~30
GET /youtube/channel/videos?continuation=TOKEN&sort=popular   # repeat tab AND sort
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `channel` | conditional | - | first page only |
| `tab` | no | `videos` | `videos` (uploads), `shorts`, `streams`. Repeat the same `tab` when paginating. |
| `sort` | no | - | `latest`, `popular`, `oldest`. Omit for the uploads feed. Repeat the same value when paginating. |
| `continuation` | conditional | - | subsequent pages |

Provide **exactly one** of `channel` or `continuation`. The response carries
`continuation_token` and `has_more`.

Existing calls are untouched: omitting sort returns the uploads feed exactly as before. sort=latest is a different view (YouTube's Videos tab, Shorts excluded), not a re-ordering of it.

| | `tab=videos`, no `sort` | `tab=videos` + any `sort` |
| --- | --- | --- |
| Source | uploads playlist | channel Videos tab |
| Page size | ~100 | ~30 |
| `playlist_info` | populated | `null` |
| Shorts | mixed in | excluded (use `tab=shorts`) |
| Members-only videos | excluded | included, flagged `members_only: true` |

They are different sets, not one list in two orders. A sorted page holds ~30 items instead of ~100, so paging a whole catalogue with `sort` set costs roughly 3.3x the pages and 3.3x the credits. Omit `sort` when you just want newest-first. `tab=shorts` / `tab=streams` read the same feed either way; there `sort` only reorders.

Every item carries `members_only`, `true` only when YouTube badges it "Members only", and those
items have no `viewCountText`. `tab=streams` items carry `lengthText` and `publishedTimeText`
(for example `Streamed 2 years ago`); `tab=shorts` returns `null` for both, because YouTube's
Shorts grid publishes neither. On the channel-tab feeds, `channelId`, `channelTitle`,
`channelHandle` and `index` are `null`.

### Search within a channel: 1 credit per page

```http
GET /youtube/channel/search?channel=@TED&q=QUERY
GET /youtube/channel/search?continuation=TOKEN
```

~30 results per page.

### Channel playlists: 1 credit per page

```http
GET /youtube/channel/playlists?channel=@TED
GET /youtube/channel/playlists?continuation=TOKEN
```

Returns id, title, URL, video-count text, thumbnails for each playlist. Pass a returned
`playlistId` to `/youtube/playlist/videos` to list its videos.

### Channel posts: 1 credit per page

```http
GET /youtube/channel/posts?channel=@TED
GET /youtube/channel/posts?continuation=TOKEN
```

Community (Posts tab) content: text, publish time, like-count text, and an `attachment`
(`image`, `multi_image`, `video`, `playlist`, or `poll`). Channels without a community tab
return an empty `results` list (HTTP 200, not an error).

### Channel sections: 1 credit

```http
GET /youtube/channel/sections?channel=@TED&tab=featured
```

| Param | Required | Default | Values |
| --- | --- | --- | --- |
| `channel` | yes | - | `@handle`, channel URL, or `UC…` ID |
| `tab` | no | `featured` | `featured` (Home), `podcasts`, `releases` |

The curated, grouped shelves of a channel page, in the channel's own order: each shelf holds
videos, playlists, shorts, or featured channels. Not paginated. `podcasts`/`releases` return
empty results on channels that don't have them.

---

## Playlists: 1 credit per page

```http
GET /youtube/playlist/videos?playlist=PL_ID        # first page
GET /youtube/playlist/videos?continuation=TOKEN    # subsequent pages
```

Valid ID prefixes: `PL`, `UU`, `LL`, `FL`, `OL`. Response includes `playlist_info`, `results`,
`continuation_token` and `has_more`. ~100 results per page.

---

## Credit costs

| Endpoint | Cost |
| --- | --- |
| `/youtube/transcript` | 1 |
| `/youtube/info` | **free** |
| `/youtube/video/metadata` | 1 |
| `/youtube/search` | 1 / page |
| `/youtube/channel/resolve` | **free** |
| `/youtube/channel/info` | 1 |
| `/youtube/channel/latest` | **free** |
| `/youtube/channel/videos` | 1 / page |
| `/youtube/channel/search` | 1 / page |
| `/youtube/channel/playlists` | 1 / page |
| `/youtube/channel/posts` | 1 / page |
| `/youtube/channel/sections` | 1 |
| `/youtube/playlist/videos` | 1 / page |

Successful requests cost 1 credit unless stated otherwise above. Failed and rate-limited requests are free.
Free endpoints still require an active plan with at least one credit available.

## Validation rules

| Field | Rule |
| --- | --- |
| `video_url` | YouTube URL (full, `youtu.be`, or shorts) or 11-character ID |
| `channel` | `@handle`, channel URL, or `UC…` ID |
| `playlist` | Playlist URL or ID with a `PL`/`UU`/`LL`/`FL`/`OL` prefix |
| `q` | 1-200 characters |
| `type` (search) | `video`, `channel`, `playlist`, `movie` |
| `tab` (channel/videos) | `videos`, `shorts`, `streams` |
| `sort` (channel/videos) | `latest`, `popular`, `oldest` (omit for the uploads feed) |
| `tab` (channel/sections) | `featured`, `podcasts`, `releases` |

## Worked example: research workflow

```bash
# 1. find candidates
curl -sG https://transcriptapi.com/api/v2/youtube/search \
  --data-urlencode "q=machine learning explained" -d type=video \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"

# 2. check languages before spending a credit (optional, free)
curl -sG https://transcriptapi.com/api/v2/youtube/info \
  --data-urlencode "video_url=VIDEO_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"

# 3. transcribe only the ones worth reading
curl -sG https://transcriptapi.com/api/v2/youtube/transcript \
  --data-urlencode "video_url=VIDEO_ID" \
  -d format=text -d include_timestamp=true -d send_metadata=true \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY" -H "User-Agent: YourAgent/1.0"
```
