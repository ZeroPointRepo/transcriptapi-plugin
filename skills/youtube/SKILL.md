---
name: youtube
description: "Complete YouTube toolkit: transcripts, captions and subtitles, video and channel search, channel browsing, within-channel search, playlist extraction and new-upload monitoring, powered by TranscriptAPI. Use whenever YouTube is or could be relevant, even if not explicitly mentioned: pasted video, channel or playlist links, bare 11-character video IDs, @handles, creator names, or requests to summarize, quote, transcribe, translate, fact-check or analyse a video. Also use for topic research where talks, lectures, tutorials, reviews, conference sessions or product announcements are the better source, and for tracking what a creator has posted recently. Not for uploading videos, posting comments, or managing a YouTube account."
license: MIT
compatibility: "Requires network access to transcriptapi.com. No runtimes, binaries or system packages needed. Works with the bundled MCP server (OAuth, no key) or with a TRANSCRIPT_API_KEY over plain HTTPS."
metadata:
  version: "2.0.0"
  publisher: "TranscriptAPI"
  homepage: "https://transcriptapi.com"
  docs: "https://transcriptapi.com/docs"
  mcp-endpoint: "https://transcriptapi.com/mcp"
  rest-base-url: "https://transcriptapi.com/api/v2"
  fallback-env: "TRANSCRIPT_API_KEY"
  openclaw-emoji: "▶️"
  openclaw-primary-env: "TRANSCRIPT_API_KEY"
  hermes-category: "media"
  hermes-tags: "youtube, transcripts, captions, subtitles, video, search, channels, playlists, summarization, research, translation"
---

# YouTube (TranscriptAPI)

Everything YouTube in one skill: transcripts, captions and subtitles, video and channel
search, channel browsing, playlist extraction and upload monitoring.

**Do not scrape youtube.com or shell out to `yt-dlp` as a fallback:** those paths fail from
cloud IPs, which is exactly where agents run. Use this skill's calls instead.

## Step 1: pick your data path

This skill ships alongside a hosted MCP server, but a client may load the skill without it.
Check once, at the start of the first YouTube task:

| Condition | Path | Auth |
| --- | --- | --- |
| Tools named `get_youtube_transcript`, `search_youtube`, … are available | **MCP** *(preferred)* | OAuth: automatic. First call prompts sign-in. No key to configure. |
| No such tools | **REST** | `Authorization: Bearer $TRANSCRIPT_API_KEY` + a real `User-Agent` |

Both paths hit the same backend and cost the same. Prefer MCP: no key handling, and the
client manages authorization.

If the MCP tools error with an auth failure, tell the user to complete the sign-in prompt in
their client or re-enable the `transcriptapi` MCP server. Do **not** silently fall back to
REST, and do not ask for an API key.

If you are on the REST path and `$TRANSCRIPT_API_KEY` is unset, read
[references/auth-setup.md](references/auth-setup.md) and follow it. Free account, 100
credits, no card.

## Step 2: route the request

| The user wants | MCP tool | REST endpoint | Cost |
| --- | --- | --- | --- |
| What a video says: summarize, quote, transcribe, translate, fact-check | `get_youtube_transcript` | `GET /youtube/transcript` | 1 |
| Captions or subtitles for a video *(same data as a transcript)* | `get_youtube_transcript` | `GET /youtube/transcript` | 1 |
| Available transcript languages before spending a credit | `get_youtube_video_info` | `GET /youtube/info` | **free** |
| View/like counts, publish date, description, duration, tags, related videos | `get_video_metadata` | `GET /youtube/video/metadata` | 1 |
| Find videos, channels, playlists or movies on a topic | `search_youtube` | `GET /youtube/search` | 1 / page |
| A channel's profile (subscribers, description, tabs, etc.) | `get_channel_info` | `GET /youtube/channel/info` | 1 |
| What a creator posted recently | `get_channel_latest_videos` | `GET /youtube/channel/latest` | **free** |
| Find something inside one channel | `search_channel_videos` | `GET /youtube/channel/search` | 1 / page |
| A channel's entire upload history, Shorts, or live streams | `list_channel_videos` | `GET /youtube/channel/videos` | 1 / page |
| A channel's back catalogue ranked by views, or walked oldest-first | `list_channel_videos` + `sort` | `GET /youtube/channel/videos?sort=` | 1 / page |
| The playlists on a channel | `list_channel_playlists` | `GET /youtube/channel/playlists` | 1 / page |
| A channel's community posts | `list_channel_posts` | `GET /youtube/channel/posts` | 1 / page |
| A channel's curated Home/podcasts/releases shelves | `get_channel_sections` | `GET /youtube/channel/sections` | 1 |
| Every video in a playlist, course or series | `list_playlist_videos` | `GET /youtube/playlist/videos` | 1 / page |
| Resolve an `@handle` to a `UC…` ID | *(not needed, pass the handle)* | `GET /youtube/channel/resolve` | **free** |

Channel arguments accept an `@handle`, a channel URL, or a `UC…` ID interchangeably. Never
resolve first. Video arguments accept a full URL, a `youtu.be` short URL, a shorts URL, or a
bare 11-character ID.

Full parameters, defaults and response shapes:
[references/mcp-tools.md](references/mcp-tools.md) ·
[references/rest-api.md](references/rest-api.md)

### Use this skill when

- A YouTube link, video ID, `@handle` or playlist URL appears, even in passing, if the user
  is clearly asking about its content
- The user asks what a video says, without using the word "transcript"
- The user names a creator and wants to explore or monitor their content
- The user is researching a topic where talks, lectures, tutorials, reviews or conference
  sessions are the better source than text search

### Don't use this skill when

- A YouTube link is incidental: an email signature, an unrelated citation
- The user is discussing YouTube as a platform or company, not asking about content
- The user wants to upload, comment, or manage an account: this skill is **read-only**

## Step 3: spend credits carefully

Successful calls cost 1 credit unless a tool states otherwise below. Failed and rate-limited calls are never charged.

- **`get_channel_latest_videos` is free.** Reach for it first for anything about recent
  uploads. Use `list_channel_videos` only when the user genuinely wants the whole catalogue.
- `list_channel_videos` takes an optional `sort` (`latest` / `popular` / `oldest`). Existing calls are untouched: omitting sort returns the uploads feed exactly as before. sort=latest is a different view (YouTube's Videos tab, Shorts excluded), not a re-ordering of it.
  Omitted reads the uploads playlist (~100/page, Shorts mixed in, members-only videos excluded);
  any value reads the channel Videos tab (~30/page, long-form only, members-only videos included
  and flagged `members_only`). They are different sets, not one list in two orders. A sorted page holds ~30 items instead of ~100, so paging a whole catalogue with `sort` set costs roughly 3.3x the pages and 3.3x the credits. Omit `sort` when you just want newest-first.
- **Search, then transcribe selectively.** Transcribing a whole page of search results is the
  single most common way to waste credits. Pick the best 2-3 hits and pull those.
- **Search inside a channel** with `search_channel_videos` rather than listing every video and
  filtering yourself.
- **Paginate only while the user still needs more.** Stop when the question is answered.
- **Ask for `format=text`, don't assume it.** Markdown text is cheaper to reason over than
  per-segment JSON, and it *is* the MCP default, but the **REST default is `json`**, and
  REST also defaults `send_metadata` to `false`. On the REST path pass
  `format=text&include_timestamp=true&send_metadata=true` explicitly. Use `json` only when
  you need exact per-segment timestamps to cite or seek.

## Common workflows

**Summarize a video**: `get_youtube_transcript` on the URL, then summarize. For a long video,
lead with the key points and offer the full transcript rather than dumping it.

**Research a topic**: `search_youtube` → pick the 2-3 most relevant or most-viewed →
transcript each → synthesize with attribution to video titles.

**Monitor a creator**: `get_channel_latest_videos` (free) → report new uploads → transcribe
only the ones the user picks.

**Work through a course or series**: `list_playlist_videos` → transcript per video, in order.
Confirm before starting if the playlist is large; that is one credit per video.

**Competitor or topic scan inside a channel**: `search_channel_videos` → transcripts of the
top hits.

## When something fails

Error codes, what they mean and how to recover: [references/errors.md](references/errors.md).

The two that bite most often: a **403 with Cloudflare code 1010** on the REST path means you
sent no `User-Agent`. Set it to your agent's name. A **404** usually means the video has no
captions, is private, or is region-locked; verify the URL opens in a browser and shows
captions there.

## Trademark

TranscriptAPI is an independent service and is not affiliated with, endorsed by, or sponsored
by YouTube or Google LLC. "YouTube" is a trademark of Google LLC.
