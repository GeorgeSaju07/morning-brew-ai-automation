# ☕ Morning Brew → LinkedIn AI Content Automation

> An AI-powered content automation pipeline that retrieves Morning Brew newsletters from Gmail, analyzes their content using Google Gemini, generates a reader-friendly LinkedIn post, and provides a structured analysis for human review.

---

## 🚀 Project Overview

Every morning, valuable information arrives in newsletters — but turning that information into meaningful professional content takes time.

This project automates that workflow.

Instead of manually reading a Morning Brew email, identifying the important information, writing a LinkedIn post, and organizing the analysis, the application performs the initial content-processing and AI-generation steps automatically.

### The workflow

```text
📧 Morning Brew
       ↓
📬 Gmail API
       ↓
🔍 Email Extraction
       ↓
🧹 Content Processing
       ↓
🤖 Google Gemini
       ↓
📊 Content Analysis
       ↓
✍️ LinkedIn Post Generation
       ↓
👤 Human Review
       ↓
🚀 LinkedIn Publishing
```

> **Current status:** The project currently automates the workflow up to AI-generated content and local output. Human review and LinkedIn API publishing are planned next.

---

## 🎯 Why This Project?

The goal is not to create a simple AI text generator.

The goal is to build a **Human-in-the-Loop AI automation system** where AI handles repetitive content-processing tasks while the human remains responsible for reviewing and approving the final content.

### The principle

```text
AI handles:
✓ Email retrieval
✓ Content extraction
✓ Content analysis
✓ Fact identification
✓ Insight generation
✓ LinkedIn draft generation

Human handles:
✓ Final review
✓ Editing
✓ Approval
✓ Publishing decision
```

This approach helps reduce repetitive work while keeping human judgment in the publishing process.

---

## ✨ Current Features

### 📬 Gmail Integration

* Connects securely to Gmail using OAuth 2.0.
* Searches for Morning Brew emails.
* Retrieves the most recent newsletter.
* Reuses stored authentication tokens.
* Automatically refreshes expired credentials when possible.

### 📄 Email Processing

* Extracts email headers.
* Handles plain-text and HTML email content.
* Recursively processes nested MIME parts.
* Converts HTML content into readable text.
* Removes unnecessary HTML elements such as scripts and styles.

### 🤖 AI Content Generation

Uses Google Gemini to analyze newsletter content and generate:

* Topic
* Key facts
* Key entities
* Main insight
* LinkedIn-ready post
* Confidence assessment

### 📊 Structured AI Output

The AI response follows a structured format:

```text
SOURCE
TOPIC
KEY_FACTS
KEY_ENTITIES
MAIN_INSIGHT
LINKEDIN_POST
CONFIDENCE
```

This makes the AI output easier to process programmatically and prepares the application for future quality-control automation.

### 💾 Local Output

The application currently generates:

```text
linkedin_post_latest.txt
linkedin_post_analysis.txt
```

The first contains the ready-to-review LinkedIn post, while the second contains the complete structured AI analysis.

---

## 🏗️ Project Architecture

The project follows a modular structure where each component has a specific responsibility.

```text
Morning-Brew-LinkedIn-Automation/
│
├── main.py
├── config.py
├── constants.py
│
├── gmail_service.py
├── gmail_processor.py
├── ai_content_generator.py
│
├── credentials.json        # Local only - not committed
├── token.json              # Local only - not committed
│
├── output/
│   ├── linkedin_post_latest.txt
│   └── linkedin_post_analysis.txt
│
├── README.md
│
└── user-guide/
    ├── ...
    └── ...
```

### Module responsibilities

| Module                    | Responsibility                                       |
| ------------------------- | ---------------------------------------------------- |
| `main.py`                 | Coordinates the complete workflow                    |
| `config.py`               | Stores configurable application settings             |
| `constants.py`            | Stores reusable application constants                |
| `gmail_service.py`        | Handles Gmail API authentication and email retrieval |
| `gmail_processor.py`      | Processes and cleans email content                   |
| `ai_content_generator.py` | Handles AI analysis and LinkedIn content generation  |

---

## 🔄 Application Workflow

### 1. Gmail Authentication

The application authenticates with Gmail using OAuth 2.0.

```text
credentials.json
       ↓
OAuth Authentication
       ↓
token.json
       ↓
Authorized Gmail Service
```

Existing tokens are reused whenever possible.

---

### 2. Newsletter Retrieval

The application searches Gmail using the configured Morning Brew search query.

```text
Gmail
  ↓
Search Morning Brew
  ↓
Latest Email
  ↓
Email Payload
```

---

### 3. Content Processing

The email payload can contain different MIME structures.

The application handles:

```text
text/plain
text/html
nested MIME parts
```

HTML content is converted into clean readable text before being sent to the AI model.

---

### 4. AI Analysis

The cleaned newsletter content is sent to Google Gemini with a structured prompt.

Gemini identifies:

```text
Topic
   ↓
Key Facts
   ↓
Key Entities
   ↓
Main Insight
   ↓
LinkedIn Post
   ↓
Confidence
```

---

### 5. Structured Response Parsing

The generated response is parsed programmatically.

Conceptually:

```python
{
    "TOPIC": "...",
    "KEY_FACTS": "...",
    "KEY_ENTITIES": "...",
    "MAIN_INSIGHT": "...",
    "LINKEDIN_POST": "...",
    "CONFIDENCE": "..."
}
```

This allows individual sections to be accessed independently.

---

## 🧠 AI Prompting Strategy

The project doesn't simply ask the model to:

> "Write a LinkedIn post."

The prompt provides specific content-generation constraints.

The AI is instructed to:

* Avoid generic AI writing patterns.
* Avoid unnecessary rhetorical questions.
* Use specific facts and numbers.
* Develop a clear point of view.
* Maintain a natural writing style.
* Avoid generic hashtags.
* Keep the LinkedIn post concise.
* Base the content on the supplied newsletter.

The goal is to produce content that feels **human-written and source-informed**, rather than a generic AI summary.

---

## 🛡️ Human-in-the-Loop Design

The application intentionally does **not** automatically publish AI-generated content at the current stage.

The intended workflow is:

```text
AI Generated Content
        ↓
Quality Validation
        ↓
Human Review
        ↓
Edit if required
        ↓
Approve
        ↓
Publish
```

This provides an additional layer of protection against:

* Unsupported claims
* Misinterpretation
* Incorrect conclusions
* AI hallucinations
* Poor-quality content

---

## 🔐 Security & Credentials

For security reasons, sensitive authentication files are intentionally not included in this repository.

The following files are excluded from GitHub:

credentials.json
token.json
.env
Why are these files excluded?
credentials.json

Contains OAuth client credentials required for Gmail API authentication.

token.json

Contains OAuth authentication information generated after successful Gmail authorization.

.env

May contain sensitive configuration values such as API keys or environment-specific settings.

These files are intentionally excluded to prevent accidental exposure of authentication credentials, access tokens, and API keys.

You must create/configure these files locally by following the setup instructions in the User Guide.

**⚠️ Never commit API keys, OAuth credentials, access tokens, or other sensitive authentication information to GitHub.**

## 📚 User Guide

This repository includes a dedicated User Guide that explains the project from both technical and non-technical perspectives.

----------

## 🛠️ Technology Stack

### Programming

* **Python**

### APIs & Services

* **Gmail API**
* **Google Gemini API**
* **LinkedIn API** *(planned)*

### Python Libraries

* `google-api-python-client`
* `google-auth`
* `google-auth-oauthlib`
* `google-genai`
* `beautifulsoup4`
* Python standard libraries such as:

  * `os`
  * `re`
  * `base64`

### Planned Technologies

* Streamlit
* LinkedIn API
* Automated scheduling
* Persistent storage
* AI quality-control layer

---

## 📈 Development Roadmap

### ✅ Phase 1 — Gmail Integration

* [x] Gmail OAuth authentication
* [x] Gmail API connection
* [x] Morning Brew email retrieval
* [x] Latest email identification

### ✅ Phase 2 — Email Processing

* [x] MIME payload processing
* [x] Plain-text extraction
* [x] HTML extraction
* [x] HTML-to-text conversion
* [x] Content cleaning

### ✅ Phase 3 — AI Content Generation

* [x] Gemini API integration
* [x] Structured prompting
* [x] Topic extraction
* [x] Key fact extraction
* [x] Entity extraction
* [x] Insight generation
* [x] LinkedIn post generation
* [x] Structured response parsing

### 🔄 Phase 4 — AI Quality Control

* [ ] Fact verification
* [ ] Unsupported claim detection
* [ ] Source alignment checking
* [ ] AI-generated content quality scoring
* [ ] Regeneration workflow

### 🔄 Phase 5 — Human Review

* [ ] Review interface
* [ ] Editable LinkedIn draft
* [ ] Approve / reject workflow
* [ ] Regeneration option

### 🔜 Phase 6 — LinkedIn Integration

* [ ] LinkedIn OAuth
* [ ] LinkedIn API integration
* [ ] Approved-post publishing
* [ ] Publishing status tracking

### 🔜 Phase 7 — Automation

* [ ] Scheduled execution
* [ ] Duplicate email detection
* [ ] Persistent processing history
* [ ] Logging
* [ ] Error handling and notifications

---

## 🔐 Security

Sensitive credentials should **never be committed to GitHub**.

The following files contain sensitive information and should remain local:

```text
credentials.json
token.json
.env
```

A `.gitignore` file should be used to prevent accidental commits.

Example:

```gitignore
credentials.json
token.json
.env
__pycache__/
*.pyc
```

API keys should be stored using environment variables rather than hardcoded in source code.

---

## 📚 Documentation

This repository also contains dedicated user guides covering the setup and usage of the application.

For detailed instructions, please refer to the documentation inside the **User Guide** folder.

The main README intentionally focuses on the project's architecture, purpose, functionality, and development roadmap.

---

## 🎯 Project Goals

This project is being developed as a practical exploration of:

* AI automation
* LLM application development
* API integration
* Prompt engineering
* Human-in-the-loop systems
* Content automation
* Python software architecture
* AI reliability and validation

The long-term goal is to evolve this from a simple script into a reliable **AI-powered content assistant**.

---

## 💡 Future Vision

The final system is intended to work as a personal AI content assistant:

```text
Morning Brew arrives
        ↓
AI discovers important stories
        ↓
AI analyzes the content
        ↓
AI identifies useful facts
        ↓
AI generates a LinkedIn draft
        ↓
AI performs quality checks
        ↓
Human reviews
        ↓
Human approves
        ↓
LinkedIn post published
```

The focus is not on removing the human from the process.

The focus is on **removing repetitive work while keeping human judgment where it matters.**

---

## 👨‍💻 Project Status

🚧 **Active Development**

This project is currently being developed incrementally, with each stage tested independently before introducing the next layer of automation.

> Built as a practical AI automation project using Python, Gmail API, and Google Gemini.
