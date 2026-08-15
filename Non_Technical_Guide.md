# Turning My Morning Brew Newsletter Into LinkedIn Posts — Automatically

## What is this?

I subscribe to **Morning Brew**, a daily business newsletter. I wanted a way to:

1. Automatically grab the latest newsletter email from my Gmail
2. Have an AI read it and turn it into a ready-to-post LinkedIn update
3. Save that post so I can review it and publish it myself

This document explains what I built, why each piece was needed, and how someone else could set up the same thing — without needing to already know how to code.

---

## The Big Picture (in plain terms)

Think of it like having a personal assistant who:
- Checks your inbox every morning
- Finds the Morning Brew email
- Reads it for you
- Writes you a draft LinkedIn post based on it
- Hands you the draft to review before you post it

Nothing gets posted automatically — I still read and publish it myself. The assistant just does the reading and drafting.

---

## What I Had to Set Up (and Why)

### Step 1: Let the assistant read my Gmail (safely)

Google doesn't let any random program read someone's email just because it asks nicely. You have to explicitly grant permission through Google's own login screen, and you can grant a **limited** kind of permission.

I set it up so the program can only ever **read** my email — it's technically incapable of sending, deleting, or changing anything, no matter what. This is similar to giving someone a key that only opens the mailbox, not the front door.

**What this took:**
- Creating a free project in Google Cloud Console (Google's control panel for developers)
- Telling Google "this app wants to read Gmail" (called enabling the Gmail API)
- Filling out a basic consent screen — just an app name and my email address
- Because this is a personal tool (not a public app reviewed by Google), I had to explicitly tell Google "I trust this app" by adding myself as a **test user**
- Downloading a small credentials file that acts like the app's ID card

**What it looks like when it works:** the first time you run the program, your browser pops open, shows the normal Google sign-in screen, and asks "allow this app to read your Gmail?" You click Allow, and you're done — it remembers you after that.

**Bumps along the way:**
- Google showed a scary-looking screen saying *"Google hasn't verified this app."* This is completely normal for a personal tool you built yourself — it's not a security warning about *this specific app* being dangerous, it just means it hasn't gone through Google's public app review (which isn't needed for something only I'm using). Clicking "Continue" was the right move.
- I got a 403 error the first time — this just meant I hadn't yet told Google "I'm allowed to test this app," which the test-user step above fixed.

### Step 2: Reading the actual newsletter content

Once permission was granted, the program:
- Searches my inbox for anything from Morning Brew
- Opens the most recent one
- Extracts the readable text from it (newsletters are actually built from a mix of formatted design elements, so the program had to specifically pull out just the words)

### Step 3: Handing it to an AI to draft a LinkedIn post

I used **Google Gemini**, a free AI model, to read the newsletter content and turn it into a post. Getting a free "API key" (basically a password that lets a program use the AI) took under two minutes at Google's AI Studio website — no credit card needed.

**Bumps along the way:**
- Google recently changed the *format* of these free API keys, and the older way of connecting to the AI stopped working with the new key format. The fix was using Google's official connection method instead of a more manual one.
- A couple of AI model versions I tried had been retired or restricted right around when I was testing — Google updates these fairly often. The fix was asking my own account directly "which AI versions can you actually use right now?" and picking one from that live list, instead of guessing from outdated instructions.

### Step 4: Making the AI's writing sound less "AI-generated"

My first draft posts had some classic AI tells — starting with a generic rhetorical question, ending with "drop your thoughts below," and using overly broad hashtags. I refined the instructions given to the AI to:
- Open with a specific fact or number instead of a generic question
- Sound like a real person's quick take, not a corporate summary
- Avoid generic filler phrases and cliché call-to-actions
- Use hashtags actually related to the topic, not generic business buzzwords

This noticeably improved how natural the posts read.

---

## End Result

Running one command now:
1. Logs into my Gmail (only the first time — after that it remembers me)
2. Grabs the latest Morning Brew email
3. Sends it to the AI with carefully tuned instructions
4. Prints a ready-to-review LinkedIn post and saves it to a text file

I then read it over, tweak anything I want, and post it myself.

---

## What This Doesn't Do (Yet)

- **It doesn't post to LinkedIn automatically.** LinkedIn requires a much more involved approval process to let outside programs publish posts on someone's behalf, so this stops at "draft ready for you to copy-paste."
- **It doesn't run on a schedule by itself** — I run it manually when I want a new post. It could be set up to run automatically every morning, which is a natural next step.

---

## Limitations (Things Worth Knowing Before Relying On This)

- **I have to log back in every so often.** Because this is a personal, unpublished tool, Google treats my login as "temporary access for testing" — it can expire after about a week, meaning I occasionally have to click through the sign-in screen again. Not a big deal, just a heads-up it's not fully "set and forget."

- **I should always read the post before publishing it.** The AI is good, but it's not perfect — it can occasionally get a detail slightly wrong or phrase something in a way I wouldn't. Nothing here checks the AI's facts against the original newsletter automatically, so a quick read-over before posting is a real step, not just a formality.

- **It only ever grabs today's (or the latest) newsletter.** If I miss running it for a few days, it won't catch me up on older issues — it just looks at whatever the most recent one is.

- **If Morning Brew changes how they design their emails, this might break.** The program is looking for specific patterns in how the newsletter is put together. If Morning Brew redesigns their email template, or starts sending from a different email address, the tool might stop finding the newsletter or start pulling in messy/irrelevant text until I update it.

- **The free AI has usage limits.** Since I'm using the no-cost tier of Google's AI, there's a cap on how many times per day I can generate a post. Running this constantly (like every hour) could hit that limit.

- **It's giving my own spin on someone else's content.** Since the post is based on Morning Brew's original newsletter, it's worth being thoughtful about it being a personal paraphrase/reaction rather than presenting it as fully original reporting — a nod to where the idea came from is good practice.

- **This only runs on my own computer, for my own account.** It's not built to be shared with other people or run automatically in the background somewhere — it's a personal tool, not a polished product.

---

## Why This Was Worth Building

Instead of manually reading the newsletter and trying to think of something interesting to say about it on LinkedIn, I now get a solid first draft handed to me in under a minute — I just review, personalize if needed, and post.
