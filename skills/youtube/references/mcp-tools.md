# MCP tool reference

The 12 tools exposed by the bundled `transcriptapi` MCP server
(`https://transcriptapi.com/mcp`, streamable HTTP, OAuth 2.1).

Authorization is handled by the client. There is no key to pass and no auth argument on any
tool. Successful calls cost 1 credit unless a tool states otherwise below; failures and rate limits are never charged.

**Which video tool?** Use `get_youtube_video_info` (free) to discover transcript languages
before fetching a transcript. Use `get_video_metadata` (1 credit) for view/like counts,
publish date, description, duration, tags, or related videos.

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

## Title: Steve Jobs' 2005 Stanford Commencement Address
## Author: Stanford

# Transcript

[0.0s] I am honored to be with you today at your commencement
[4.12s] from one of the finest universities in the world.
```

**`format="json"`**

```json
{
  "video_id": "UF8uR6Z6KLc",
  "language": "en",
  "transcript": [
    { "text": "I am honored to be with you today at your commencement", "start": 0.0, "duration": 4.12 },
    { "text": "from one of the finest universities in the world.", "start": 4.12, "duration": 3.85 }
  ],
  "metadata": {
    "title": "Steve Jobs' 2005 Stanford Commencement Address",
    "author_name": "Stanford",
    "author_url": "https://www.youtube.com/@stanford",
    "thumbnail_url": "https://i.ytimg.com/vi/UF8uR6Z6KLc/maxresdefault.jpg"
  }
}
```

---

## `get_youtube_video_info`: FREE

Basic metadata (title, author, thumbnail) plus the list of available transcript languages:
call this before `get_youtube_transcript` to pick a language.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `video_url` | string | **required** | Full URL, short URL, or bare 11-character video ID |

Each returned language code (e.g. `en`, or `asr-en` for auto-generated English) can be passed
to `get_youtube_transcript`'s `language` parameter. For counts, publish date, description,
duration, tags, or related videos, use `get_video_metadata` instead.

---

## `get_video_metadata`: 1 credit

Rich video metadata without needing captions: title, view/like-count text, publish date, a
structured description with extracted links, an uploading-channel summary, and thumbnails.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `video_url` | string | **required** | Full URL, short URL, or bare 11-character video ID |
| `include` | string[] | _none_ | `"details"` (duration, category, tags, caption tracks) and/or `"related"` (related videos) |

Hidden counts are `null`, never `0`. When `details` can't be read, `details.available` is
`false` with a `reason` instead of a guessed value.

```json
get_video_metadata({ video_url: "UF8uR6Z6KLc", include: ["details", "related"] })
```

---

## `search_youtube`: 1 credit per page

Search YouTube for videos, channels, playlists, or movies. ~20 results per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `query` | string | **required** (first call) | 1-200 characters |
| `search_type` | string | `"video"` | `"video"`, `"channel"`, `"playlist"`, or `"movie"` (first call only) |
| `sort` | string | `"relevance"` | `"relevance"` or `"views"` (first call only) |
| `upload_date` | string | _none_ | `hour`, `today`, `week`, `month`, `year` (first call, videos only) |
| `duration` | string | _none_ | `short` (under 4m), `medium` (4-20m), `long` (over 20m) (first call, videos only) |
| `continuation` | string | `null` | Token from a prior call, for the next page |

Provide either `query` (first call) or `continuation` (next pages), not both. Filters apply to
the first call only; the `continuation` token already encodes them. Returns metadata only, no
transcripts. Pick the best hits, then transcribe those.

---

## `get_channel_info`: 1 credit

A channel's profile: title, `@handle`, verified flag, subscriber/video-count text, description,
keywords, tags, thumbnails, banners, and the tabs it exposes. Not paginated.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |

Counts are display strings (e.g. `27.8M subscribers`) and `null` when YouTube hides them,
never `0`. Check `availableTabs` before calling `get_channel_sections` or `list_channel_videos`
with a `tab`.

---

## `get_channel_latest_videos`: FREE

The ~15 most recent uploads from a channel, via RSS.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |

Use it freely for anything about recent uploads, monitoring, or daily recaps.
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

A channel's feed, paginated. Use `tab` to choose the uploads feed (default, ~100/page), Shorts,
or live streams (~48/page).

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `tab` | string | `"videos"` | `videos` (uploads), `shorts`, or `streams`. Repeat the same `tab` when paginating. |
| `continuation` | string | `null` | Pagination token |

Only when the user genuinely wants the whole catalogue. For recent uploads use
`get_channel_latest_videos` (free); to find something specific use `search_channel_videos`.

---

## `list_channel_playlists`: 1 credit per page

Paginated list of the playlists on a channel (id, title, URL, video-count text, thumbnails).

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null` | Pagination token |

Pass a returned playlist id to `list_playlist_videos` to get its videos.

---

## `list_channel_posts`: 1 credit per page

Paginated list of a channel's community (Posts tab) content: text, publish time, like-count
text, and attachments (image, multi-image, video, playlist, or poll).

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** (first call) | `@handle`, channel URL, or `UC…` ID |
| `continuation` | string | `null` | Pagination token |

Channels without a community tab return an empty results list (not an error).

---

## `get_channel_sections`: 1 credit

The curated, grouped sections of a channel page: titled shelves of videos, playlists, shorts,
or featured channels, in the channel's own order. Not paginated.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `channel` | string | **required** | `@handle`, channel URL, or `UC…` ID |
| `tab` | string | `"featured"` | `featured` (Home), `podcasts`, or `releases` |

`podcasts` and `releases` exist only on channels that have them (empty results otherwise: call
`get_channel_info` to see a channel's tabs first).

---

## `list_playlist_videos`: 1 credit per page

Every video in a playlist, ~100 per page.

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `playlist` | string | **required** (first call) | Playlist URL or ID: `PL`, `UU`, `LL`, `FL`, `OL` prefixes |
| `continuation` | string | `null` | Pagination token |

Confirm before transcribing a large playlist: that is one credit per video.
