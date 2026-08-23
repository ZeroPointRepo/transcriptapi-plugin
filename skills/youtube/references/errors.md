# Errors and recovery

Error codes come from the API itself and surface on both the MCP and REST paths.

| Code | Meaning | What to do |
| --- | --- | --- |
| `401` | Bad or missing credentials | **MCP:** tell the user to complete the sign-in prompt, or re-enable the `transcriptapi` server in their client. **REST:** confirm `$TRANSCRIPT_API_KEY` is set in the shell your agent runs in and starts with `sk_`. Never fall back from MCP to asking for a key. |
| `402` | Out of credits | Tell the user to top up at <https://transcriptapi.com/billing>. Do not retry. |
| `403` (Cloudflare `1010`) | No `User-Agent` header — REST path only | Set `User-Agent` to your agent's name, e.g. `ClaudeCode/1.0`, and retry once. |
| `404` | Video/channel/playlist not found, or no captions | The video may have no captions, be private, age-restricted or region-locked. Verify the URL opens in a browser **and shows captions there**. Don't retry — report it. |
| `408` | Upstream timeout | Transient. Retry **once** after ~2 seconds, then report. |
| `422` | Malformed parameter | Check the reference: channels take `@handle`/URL/`UC…`; playlists take `PL`/`UU`/`LL`/`FL`/`OL`; `q` is 1–200 chars; `limit` is 1–50. |
| `429` | Rate limited | Wait and respect the `Retry-After` header. Not charged. |

## Situations that look like errors but aren't

**Live streams and premieres.** Transcripts only exist after the stream ends and captions
finish processing. A 404 on a currently-live video is expected — say so rather than retrying.

**Unexpected transcript language.** Many videos carry captions only in their original
language. That's the source data, not a bug. Translate the result yourself if the user wants
another language.

**Empty or very short transcript.** Some videos have auto-captions disabled or only a few
seconds of speech. Check `metadata.title` to confirm you fetched the right video before
assuming a failure.

**The key is set but the agent can't see it (REST path).** Shell config files load per shell
type. Confirm the file matches the shell your agent actually runs in — see
[auth-setup.md](auth-setup.md) — and restart the agent after saving.

## Retry policy

Retry **once** on `408`. Respect `Retry-After` on `429`. Never auto-retry `401`, `402`, `404`
or `422` — they will not resolve on their own, and repeated `4xx` calls just add latency.
Failed requests never consume credits, so a single well-chosen retry is free.
