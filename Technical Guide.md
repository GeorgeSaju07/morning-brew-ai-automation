# Morning Brew → LinkedIn Automation (Technical README)

## 1. Overview

This project is a small automation pipeline that:

1. Authenticates to a personal Gmail account via OAuth2 and the **Gmail API** (read-only scope).
2. Searches the mailbox for emails from **Morning Brew** and extracts the latest one's content.
3. Sends that content to a **free-tier LLM (Google Gemini)** with a tuned prompt to generate a publish-ready LinkedIn post.
4. Saves the generated post locally for manual review/posting (no auto-publish to LinkedIn — see [Non-Goals](#7-non-goals--future-work)).

Three scripts make up the project:

| File | Purpose |
|---|---|
| `morning_brew_extractor.py` | Bulk-extracts all matching Morning Brew emails to local `.txt`/`.html` files |
| `morning_brew_to_linkedin.py` | Fetches the single latest Morning Brew email and generates a LinkedIn post via Gemini |
| `list_gemini_models.py` | Diagnostic script — lists which Gemini models the current API key/account can actually call |

---

## 2. Architecture

```
┌─────────────┐      OAuth2       ┌──────────────┐
│   Script    │ ───────────────►  │  Gmail API   │
│ (Python)    │ ◄─────────────── │ (googleapis) │
└─────┬───────┘   messages.list/   └──────────────┘
      │           messages.get
      │ raw MIME payload (base64)
      ▼
┌─────────────┐
│ MIME parser │  recursive walk of payload.parts
│ (stdlib)    │  → plain_text / html_text
└─────┬───────┘
      │ HTML → clean text (BeautifulSoup, if no plain-text part)
      ▼
┌─────────────┐    REST/SDK call   ┌────────────────┐
│   Prompt    │ ─────────────────► │  Gemini API     │
│  template   │ ◄───────────────── │ (generateContent)│
└─────┬───────┘   generated text   └────────────────┘
      ▼
┌─────────────┐
│ Local file  │  linkedin_post_latest.txt
└─────────────┘
```

---

## 3. Gmail OAuth2 Setup (Google Cloud Console)

The Gmail API requires an OAuth2 **Desktop app** client, not just an API key, because it accesses user-specific data (the mailbox) rather than public data.

### 3.1 Enable the API
1. Create/select a project at [console.cloud.google.com](https://console.cloud.google.com).
2. **APIs & Services → Library** → search "Gmail API" → **Enable**.

### 3.2 Configure the OAuth consent screen
1. **APIs & Services → OAuth consent screen**.
2. **User Type**: External (required for personal/non-Workspace Gmail accounts).
3. Fill in:
   - **App name**: any label (e.g. "Morning Brew Extractor")
   - **User support email**: your own address
4. Because the app is unverified (a personal script, not a published product), it stays in **Testing** mode. In Testing mode, Google restricts sign-in to explicitly whitelisted accounts:
   - Go to the **Audience** / **Test users** section → **Add users** → add your own Gmail address.
   - Testing-mode restriction means refresh tokens are also short-lived (~7 days) unless the app is later verified — acceptable for personal/dev use, not for production distribution.

### 3.3 Create OAuth client credentials
1. **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
2. **Application type**: `Desktop app`. This matters because Desktop app clients use the **loopback redirect** flow (`http://localhost:<random_port>`), which `google-auth-oauthlib`'s `InstalledAppFlow.run_local_server()` handles automatically — no manual redirect URI configuration needed, unlike Web application clients.
3. Download the JSON → rename to `credentials.json` → place alongside the scripts.

### 3.4 OAuth flow at runtime
```python
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())          # silent refresh, no browser
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)   # opens browser, spins up local server
    with open("token.json", "w") as f:
        f.write(creds.to_json())
```

- `run_local_server(port=0)` binds an ephemeral local port, opens the system browser to Google's consent screen, and captures the authorization `code` redirected back to `http://localhost:<port>/?code=...`.
- The code is exchanged server-side (by the library) for an **access token** + **refresh token**, both persisted in `token.json`.
- Subsequent runs skip the browser entirely and silently refresh the access token using the refresh token, as long as it hasn't been revoked or expired (Testing-mode tokens: ~7 days).

**Scope used**: `gmail.readonly` — read-only. This is a hard constraint at the token level; the credential physically cannot call mutating endpoints (`send`, `trash`, `modify`, etc.) regardless of application logic.

---

## 4. Gmail API Data Retrieval

### 4.1 Search
```python
service.users().messages().list(userId="me", q=SEARCH_QUERY, maxResults=N).execute()
```
- Uses standard Gmail search syntax (`from:(...)`) via the `q` parameter — identical to the Gmail UI search bar.
- Returns lightweight `{id, threadId}` references only, **not** message content. Pagination via `nextPageToken` when result sets exceed ~100.

### 4.2 Fetch
```python
service.users().messages().get(userId="me", id=msg_id, format="full").execute()
```
- `format="full"` returns the complete MIME structure as nested JSON (`payload.parts[]`), plus headers (`Subject`, `From`, `Date`, etc.) as a flat list under `payload.headers`.

### 4.3 MIME body extraction
Email bodies are a **tree**, not a flat structure (multipart/alternative, multipart/related, nested parts for plain-text vs HTML vs attachments). The extractor recursively walks `payload.parts`:

```python
def walk(part):
    mime_type = part.get("mimeType", "")
    body_data = part.get("body", {}).get("data")
    if body_data:
        decoded = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="replace")
        if mime_type == "text/plain": plain_text += decoded
        elif mime_type == "text/html": html_text += decoded
    for sub_part in part.get("parts", []):
        walk(sub_part)
```

- Gmail transmits body content **Base64url-encoded** inside JSON (binary-safe transport) — must be decoded before use.
- When no `text/plain` part exists (common for marketing HTML emails like Morning Brew), the pipeline falls back to stripping the HTML via BeautifulSoup (`get_text()`), collapsing redundant whitespace with regex.

---

## 5. LLM Integration (Google Gemini)

### 5.1 Why Gemini
Chosen for a genuinely free tier accessible via a single API key from [Google AI Studio](https://aistudio.google.com/apikey), no billing account required at time of writing.

### 5.2 Authentication — API key format change (as of 2026)
Google has been transitioning Gemini API keys from the legacy `AIzaSy...` format to a new `AQ.`-prefixed **Authentication Key** format. This is significant because:

- `AQ.` keys are **not** reliably compatible with raw REST calls using `?key=<key>` query-string auth (`requests.post(url, params={"key": ...})`), which is how the original REST-based implementation was written — it failed with `401 UNAUTHENTICATED` / `ACCESS_TOKEN_TYPE_UNSUPPORTED`.
- **Fix**: use the official `google-genai` Python SDK (`pip install google-genai`), which correctly negotiates auth for both key formats:

```python
from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
text = response.text
```

### 5.3 Model selection — handling deprecation churn
Model availability has shifted multiple times over the course of this project:
- `gemini-2.0-flash` → retired (shutdown June 2026).
- `gemini-2.5-flash` → returned `404 NOT_FOUND` ("no longer available to new users") on a freshly created account, despite being listed as generally available for existing accounts.

**Mitigation implemented**: `list_gemini_models.py` calls `client.models.list()` and filters for models where `"generateContent" in model.supported_actions`, giving ground truth for what the *current* API key can actually invoke, rather than hardcoding a model name from documentation that may be stale.

**Final model used**: `gemini-flash-lite-latest` — an alias Google maintains that points to their current recommended fast/cheap model, intended to reduce the need for manual updates as underlying model versions rotate. Pinning to a versioned name (e.g. `gemini-3.6-flash`) is more predictable for reproducibility but requires manual updates when Google deprecates it; the `-latest` alias trades reproducibility for lower maintenance.

Google is also rolling out a separate **Interactions API** (`client.interactions.create`) as the long-term replacement for `generateContent`, but as of this writing `generateContent` remains fully supported, so the pipeline was not migrated.

### 5.4 Prompt design
The prompt (`generate_linkedin_post()`) is intentionally over-specified to counter common LLM-generated-content tells:

| Pattern suppressed | Constraint added |
|---|---|
| Rhetorical-question hooks ("Are shoppers tapping out?") | Explicit ban; require opening with a concrete fact/number |
| Generic transition phrases ("Here's the thing", "It makes you wonder") | Explicit ban list |
| Generic CTA ("Drop your thoughts below") | Require a topic-specific closing question |
| Generic/broad hashtags (#BusinessInsights, #MarketTrends) | Require hashtags tied to specific entities/topics in the source |
| Uniform paragraph rhythm | Explicit instruction to vary sentence/paragraph length |

Content length is truncated to 12,000 characters before prompting to stay within free-tier token budgets on long newsletters.

---

## 6. Environment & Dependencies

```bash
pip install --break-system-packages \
    google-auth-oauthlib google-auth-httplib2 google-api-python-client \
    google-genai beautifulsoup4
```

**Environment variable**:
```
GEMINI_API_KEY=<key from https://aistudio.google.com/apikey>
```
- On Windows, `setx` persists the variable to the user registry but does **not** propagate to already-running processes (e.g. an open IDE) — the IDE/terminal must be restarted, or the variable set directly in the IDE's run configuration.
- Recommended longer-term: a `.env` file + `python-dotenv`, to avoid IDE-restart dependency and keep the key out of shell history.

**Local files generated at runtime** (not checked into version control):
- `token.json` — OAuth refresh/access tokens
- `credentials.json` — OAuth client secret (download from Cloud Console)
- `morning_brew_emails/` — bulk-extracted email archive
- `linkedin_post_latest.txt` — most recent generated post

Add all of the above to `.gitignore`.

---

## 7. Non-Goals / Future Work

- **No auto-posting to LinkedIn.** LinkedIn's official API for publishing posts (`ugcPosts`/`posts` endpoint under the Marketing/Community Management API) requires an approved developer application and product access review — out of scope for a personal script. Current design intentionally stops at "generate text for manual review/paste."
- **No scheduling.** Script is invoked manually; could be wrapped in a cron job / Windows Task Scheduler, keeping in mind the ~7-day token expiry under OAuth Testing mode.
- **No verification of Google Cloud OAuth app.** Staying unverified is fine for single-user personal use; would require Google's verification review to scale beyond a handful of test users.

---

## 8. Limitations

**Auth / access**
- OAuth app stays in **Testing** mode indefinitely (by design, for a personal tool). This means: only whitelisted test users can authenticate, and refresh tokens can expire in as little as ~7 days, requiring periodic re-authentication via browser. Not suitable as-is for distribution to other users.
- `credentials.json` and `token.json` are plaintext local files with no encryption at rest. Anyone with filesystem access to the machine can extract them and impersonate the OAuth client / reuse the session. Not committed to git, but also not protected beyond OS-level file permissions.

**Model / AI dependency**
- Hardcoded to a single provider (Gemini). No fallback if Gemini has an outage, changes its free-tier terms, or further changes API key formats — as already happened twice during development.
- Free-tier Gemini usage is rate-limited (requests/day and requests/minute caps that vary by model and can change without notice). Running the script frequently (e.g. hourly via a scheduler) risks hitting these limits.
- Model names/aliases used (`gemini-flash-lite-latest`) are Google-managed pointers that can silently change behavior/quality when Google updates what they point to — output quality isn't pinned to a fixed model version.
- No fact-checking or hallucination safeguard. The AI paraphrases the newsletter, but nothing in the pipeline verifies factual accuracy of the generated post against the source before it reaches the output file. Manual review before posting is required, not optional.

**Content pipeline**
- Search query (`from:(morningbrew.com OR ...)`) is a static string. If Morning Brew changes sending domains/addresses (they already vary by sub-newsletter — Daily, Retail, Marketing, etc.), matching emails will silently stop being found with no error raised.
- HTML-to-text extraction (BeautifulSoup `get_text()`) is a generic parser, not tuned to Morning Brew's specific template. If Morning Brew changes their email layout, extraction quality (ad content, image captions, or navigation boilerplate leaking into the "content") could degrade without warning.
- Only ever processes the single most recent matching email (`morning_brew_to_linkedin.py`). No handling for "what if the newsletter didn't arrive today" or catching up on missed days.
- No retry/backoff logic around either the Gmail API or Gemini API calls — a transient network failure or rate-limit response simply crashes the script (stack trace to console), rather than retrying or failing gracefully.

**Content/legal**
- Output is AI-paraphrased content derived from a copyrighted third-party newsletter. Publishing paraphrased summaries of Morning Brew's original reporting/analysis on LinkedIn under one's own name carries some attribution/fair-use considerations worth being deliberate about — this pipeline doesn't include any attribution-back-to-source step.
- No de-duplication check — running the script twice on the same day (before a new newsletter arrives) will regenerate a post from the same source email, potentially producing near-duplicate content.

**Operational**
- Single-threaded, single-user, local-machine execution only — no persistence layer, database, or multi-account support.
- Tested on Windows/PyCharm during development; paths and `setx` guidance are Windows-specific, though the underlying Python/API code is cross-platform.

---

## 9. Troubleshooting Log (issues actually hit during development)

| Symptom | Root cause | Fix |
|---|---|---|
| "An error occurred while creating the OAuth configuration" | Transient Cloud Console error | Retry; confirm a project is selected; try incognito/different browser |
| `Error 403: access_denied` on consent screen | App in Testing mode, user not whitelisted | Add account under OAuth consent screen → Audience → Test users |
| "Google hasn't verified this app" warning | Expected behavior for unverified Testing-mode apps | Click Continue (safe — you're the developer/test user) |
| `401 Unauthorized` / `ACCESS_TOKEN_TYPE_UNSUPPORTED` calling REST endpoint directly | New `AQ.`-format API keys incompatible with raw `?key=` REST auth | Switch to `google-genai` SDK client instead of `requests` |
| `404 NOT_FOUND: gemini-2.0-flash` | Model retired June 2026 | Update `GEMINI_MODEL` to a current model |
| `404 NOT_FOUND: gemini-2.5-flash ... no longer available to new users` | Model access varies by account creation date/tier | Run `list_gemini_models.py` to get ground-truth available models for the current key |
