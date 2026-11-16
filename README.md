# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small backend a writing site could plug in. A piece of
writing goes in; what comes back is a guess (`ai` / `human` / `unsure`), a 0–1
score, a sentence a reader can understand, and a way for the writer to contest
it. The path one submission takes (my Milestone 1 trace is in
[design.md](design.md)):

1. **The route checks the request** (`app.py::submit`, `_check_submission`).
   The body must be a JSON object (at most 200 KB) with `text` (a non-blank
   string, at most 20,000 characters, at least 10 words) and `creator_id` (a
   non-blank string with no control or line-break characters).
   Anything else is refused with a 4xx JSON error and logged as `rejected`
   before any model runs. A good request gets a fresh `content_id`.
2. **Signal one reads the text** (`detector.py::model_signal`). gpt2, running
   locally, measures how predictable the text is, giving `model_score`, 0–1,
   higher = more AI-like.
3. **Signal two measures its shape** (`stylometry.py::style_signal`):
   sentence-length spread, vocabulary variety and expressive punctuation give
   `style_score`, 0–1, higher = more AI-like.
4. **The combining rule makes one number** (`scoring.py::combine_signals`):
   the average of the two, with a cap that stops the AI label unless *both*
   signals lean AI. This is `confidence`.
5. **The label mapping turns it into words** (`scoring.py::score_to_label`).
   One of three full sentences, below.
6. **The decision is logged** (`audit.py::log_decision`). One JSON line in
   `logs/audit.jsonl` with the timestamp, both ids, both signal scores, the
   combined score, guess, label and `status: "decided"`.
7. **The response goes back** with all of that, plus a line on how to appeal.
8. **If the writer disagrees** they `POST /appeal` with the `content_id`,
   their `creator_id` and their reasons (`app.py::appeal`). The service checks
   the item exists, belongs to that creator (so nobody reading `/log` can use up
   a stranger's one appeal), and isn't already under review, appends an
   `appeal` entry with
   `status: "under_review"` next to the untouched original decision, and
   confirms.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** perplexity under gpt2, i.e. how surprised a language
model is by each next word, squashed to 0–1 (perplexity 45 → 0.5; lower
perplexity → higher score). Given in `detector.py`; I didn't move its midpoint.

**Why that might differ between human and AI writing:** a model writes by
picking likely next words, so text a model wrote tends to be text a model
finds easy to predict. People make stranger choices.

**What it can't see:** authorship. It rewards *common words in ordinary
sentences*, and plenty of people write that way: second-language writers,
young writers, anyone writing plainly. In my calibration the plain opening of
*The Wonderful Wizard of Oz* (1900) scored **0.71** and the Gettysburg Address
**0.73** — about as machine-like as my clearly-AI paragraphs (0.81–0.89).
(Gettysburg is also almost certainly memorised by gpt2, which makes famous
human text look predictable.) The reverse failure is just as real: an AI
paragraph I prompted to use rare, ornate words scored **0.17**, firmly
"human". It only reads the first 400 tokens.

### Signal two — the style signal

**What it measures** (`stylometry.py`), three measures with no understanding
of a word:

| measure | how | direction |
|---|---|---|
| sentence-length spread | std-dev ÷ mean of words per sentence | higher = more human |
| vocabulary variety | moving-average type-token ratio over 40-word windows (so length doesn't decide it) | **higher = more AI** (see below) |
| expressive punctuation | `; : ! ? ( ) — – - " '` and `…` per 100 words (full stops and commas left out) | higher = more human |

Each is mapped onto 0–1 "AI-ness" by a straight ramp between two anchors set
from calibration — spread AI at 0.20 / human at 0.70; variety AI at 0.93 /
human at 0.75; punctuation AI at 0.5 / human at 6.0 — and then averaged
0.40 / 0.35 / 0.25. A measure that can't be computed (one sentence, under 10
words) drops out and the others are re-weighted; if none can be computed the
signal says 0.5, "no evidence".

**Why that might differ between human and AI writing:** generated prose
marches in even, mid-length sentences with tidy punctuation; human writing is
lumpy (a three-word sentence next to a forty-word one, dashes, asides,
contractions). *A finding I didn't expect:* the starter's hint says AI text
has a narrower vocabulary, but on paragraph-length text mine ran the other
way. My three AI paragraphs had a moving-average TTR of 0.89–0.93, the human
ones 0.74–0.83, because short AI prose is dense with distinct content words
while people repeat little words ("he told the truth, mainly … mainly he told
the truth"). So I followed the data and flipped that measure. It may not hold
on long texts, which is a thing for unit 8 to check.

**What it can't see:** meaning. Anything that changes the shape without the
substance moves it: splitting sentences, adding typos, sprinkling in dashes
or a question mark. My lightly-edited AI paragraph (contractions, a dash, a
"Honestly?") dropped from ~0.9 to **0.38** on this signal. A careful human
writer with very even sentences, which describes a lot of formal and
technical writing, looks AI to it (Gettysburg: 0.53, Oz: 0.61). On very short
text it has almost nothing to measure.

### The combining rule

**The rule:** take the plain average of the two signals. Then, **if either
signal on its own is below 0.65, cap the result at 0.69**, one point under
the AI line. In words: the system may only say "this is AI" when both methods
independently lean AI. When they disagree, that disagreement *is* the
uncertainty, and uncertainty is never allowed to come out as an accusation.
The cap only works in the accusing direction; being wrongly called human is
the cheap mistake on a writing site, so there's no matching floor.

**The numbers** (`config.py`): `WEIGHT_MODEL_SIGNAL = 0.5`,
`WEIGHT_STYLE_SIGNAL = 0.5`, `AGREEMENT_FLOOR = 0.65`,
`HUMAN_THRESHOLD = 0.40`, `AI_THRESHOLD = 0.70`. My Milestone 1 guess was an
AI line at 0.75 with a 0.60 floor. Calibration moved them: every unedited AI
paragraph had both signals ≥ 0.75 and combined ≥ 0.79, while the plain Oz
passage had model 0.71 / style 0.61. A floor of 0.65 holds that passage at
"unsure" without letting obvious AI through.

**Where it lives:** `scoring.py::combine_signals` (weights and thresholds in
`config.py`).

**Calibration run** (`python calibration.py`). AI texts generated by Claude
from plain prompts, human texts public-domain published prose:

| text | model | style | combined | guess |
|---|---|---|---|---|
| AI: time management | 0.819 | 0.802 | 0.810 | ai |
| AI: social media | 0.814 | 0.925 | 0.869 | ai |
| AI: exercise | 0.892 | 0.876 | 0.884 | ai |
| ornate AI: lighthouse ledger | 0.170 | 0.740 | 0.455 | unsure |
| edited AI: social media | 0.504 | 0.378 | 0.442 | unsure |
| human: Huckleberry Finn (1884) | 0.463 | 0.020 | 0.242 | human |
| formal human: Gettysburg (1863) | 0.727 | 0.534 | 0.631 | unsure |
| plain human: Wizard of Oz (1900) | 0.713 | 0.614 | 0.664 | unsure |

**A case where my two signals split, and what my rule does with it:** the
ornate AI paragraph. Signal one says **0.17** (rare words surprised gpt2, so
"human"); signal two says **0.74** (even sentences, little expressive
punctuation, very varied vocabulary, so "AI"). The average is 0.455, unsure,
which is what I want: one method says human and one says AI, and the honest
answer is "we can't tell". The cap is for the opposite split, where the score
alone would cross the line. A text at model 0.95 / style 0.55 averages 0.75,
which would be an accusation. Style is under 0.65, so the rule caps it at
**0.69 → unsure**. That shape is the plain human writer: gpt2 is sure, the
shape is ordinary. The cost is that AI text which fools one signal, like the
lightly-edited paragraph, gets "unsure" instead of "ai". I accept that trade.

---

## Label Variants

Bands are half-open, so every score lands in exactly one (`python scoring.py`
checks all 101 values from 0.00 to 1.00).

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – under 0.40 | We think a person wrote this. Our automated check found the kind of variety we usually see in human writing. |
| unsure | 0.40 – under 0.70 (and anything capped by the agreement rule) | Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result. |
| high-confidence AI | 0.70 – 1.00, and only if both signals are ≥ 0.65 | Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it. |

All three were reached through the real `/submit` route: an AI paragraph got
`ai` (0.79), the Oz passage `unsure` (0.66), and the Huckleberry Finn opening
`human` (0.30). Every response also carries an `appeal` line telling the
writer how to contest it, whatever the label.

**Why I worded the "unsure" one this way:** the person most likely to see it
is the plain writer that signal one can't tell from a machine, the one my
false-positive trace followed. So it does three things in order: says
plainly that *the check* failed, not the writer ("couldn't tell"); tells them
this is common and names the reason, plain writing, so a second-language
writer reading it knows it isn't about them; and says outright that
nothing happens because of it, which is the first question anyone asks. It
never uses "suspicious", "flagged" or a number. The AI label says "may have
been" and "not proof", because at best this is a strong guess, and it puts
the way out (a human review) in the same sentence a writer reads first.

---

## Sample Run

Run against the service on `127.0.0.1:5000` from Git Bash, with the request
bodies in files (`-d @file`) to keep the quoting readable. The text is the
public-domain opening of *The Wonderful Wizard of Oz* (L. Frank Baum, 1900),
the kind of plain human writing signal one can't tell from a machine; the
appeal says so.

**A submission**

```bash
$ cat sub.json
{"text": "Dorothy lived in the midst of the great Kansas prairies, with Uncle Henry, who was a farmer, and Aunt Em, who was the farmer's wife. Their house was small, for the lumber to build it had to be carried by wagon many miles. There were four walls, a floor and a roof, which made one room; and this room contained a rusty looking cookstove, a cupboard for the dishes, a table, three or four chairs, and the beds.", "creator_id": "baum_1900"}
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d @sub.json
```

```json
{
  "appeal": "Wrote this yourself and think the label is wrong? Send POST /appeal with this content_id, your creator_id and a sentence or two on why.",
  "confidence": 0.6638,
  "content_id": "adadf83002434c699e0ba6a12886e506",
  "creator_id": "baum_1900",
  "guess": "unsure",
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "model_score": 0.7134,
  "status": "decided",
  "style_score": 0.6141
}
```

**An appeal**

```bash
$ cat appeal.json
{"content_id": "adadf83002434c699e0ba6a12886e506", "creator_id": "baum_1900", "reasoning": "This is the opening paragraph of The Wonderful Wizard of Oz by L. Frank Baum, published in 1900. A person wrote it more than a century before language models existed. It is plain because it was written for children."}
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d @appeal.json
```

```json
{
  "appealed_at": "2026-11-15T21:50:46+00:00",
  "content_id": "adadf83002434c699e0ba6a12886e506",
  "message": "Thanks — your appeal is recorded and this piece is now under review. A person will look at it; until then the label is marked as disputed.",
  "original": {
    "confidence": 0.6638,
    "decided_at": "2026-11-15T21:50:46+00:00",
    "guess": "unsure",
    "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result."
  },
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.6638,
      "content_id": "adadf83002434c699e0ba6a12886e506",
      "creator_id": "baum_1900",
      "guess": "unsure",
      "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
      "model_score": 0.7134,
      "status": "decided",
      "style_score": 0.6141,
      "text_length": 408,
      "timestamp": "2026-11-15T21:50:46+00:00"
    },
    {
      "content_id": "adadf83002434c699e0ba6a12886e506",
      "creator_id": "baum_1900",
      "event": "appeal",
      "reasoning": "This is the opening paragraph of The Wonderful Wizard of Oz by L. Frank Baum, published in 1900. A person wrote it more than a century before language models existed. It is plain because it was written for children.",
      "status": "under_review",
      "timestamp": "2026-11-15T21:50:46+00:00"
    }
  ]
}
```

The original decision is still there, unchanged, with the appeal after it.
The appeal path's refusals, from the same run:

```text
same appeal again            -> 409 {"error": "already_under_review", "message": "This piece is already under review. Your first appeal is on record."}
content_id "not-a-real-id"   -> 404 {"error": "unknown_content_id", "message": "We have no submission with content_id 'not-a-real-id' under that creator_id. Check both were copied exactly."}
someone else's creator_id    -> 404 {"error": "unknown_content_id", "message": "We have no submission with content_id 'adadf83002434c699e0ba6a12886e506' under that creator_id. Check both were copied exactly."}
no reasoning                 -> 400 {"error": "missing_reasoning", "message": "Tell us in a sentence or two why you think the label is wrong."}
```

Each of those also left a `rejected` entry in the log, keyed by
`target_content_id` so it never joins the item's own history.

**Bad input** (criterion 5's nine bodies plus four extras, against `/submit`):

```text
text missing             400 missing_text
text empty               400 empty_text
text whitespace          400 empty_text
text null                400 missing_text
text 42                  400 missing_text
body is a list           400 invalid_json
creator missing          400 missing_creator_id
20,001 chars             413 text_too_long
50,000 words             413 request_entity_too_large
(extra) not JSON         400 invalid_json
(extra) '!!! ??? ...'    422 text_too_short
(extra) 'Hi there'       422 text_too_short
(extra) nested [[[…      400 invalid_json
-> 0 responses were 5xx; 13 new rejected entries in the log for 13 requests; /ping answered {"ok": true, "service": "provenance-guard", "you_sent": "still alive"}
```

---

## How I Used AI

I wrote all five acceptance criteria myself. I used Claude to put them into
the repo and help with the wording, but the README incorrectly said Claude
wrote them. I used Codex to correct that and clean up the wording. The targets
and test requirements are still the same as in the first criteria commit.

I used Claude Code (Claude Opus) to help build the rest of this unit: the
Milestone 1 trace, both routes, the style signal, the combining rule, the
labels, and this write-up. It worked milestone by milestone and committed
after each one. The criteria commit comes before any scoring code ran.
Two examples of how I used its output:

**Moment 1: the vocabulary measure ran backwards**

- *What I asked for:* build the three stylometry measures and calibrate them
  on clearly-AI, clearly-human, plain-human and lightly-edited-AI text.
- *What came back:* the first version followed the starter's hint (AI = less
  varied vocabulary), with anchors guessed in advance. The calibration table
  showed the opposite: AI paragraphs had a moving-average type-token ratio of
  0.89–0.93, human ones 0.74–0.83. With the hinted direction, the measure was
  calling every AI paragraph human.
- *What I changed:* flipped that measure's anchors to follow the data,
  documented the finding in `stylometry.py::type_token_ratio` and above, and
  flagged that it may not hold on long texts. That's something to test in
  unit 8 instead of assume.

**Moment 2: the plain human writer, and the agreement rule**

- *What I asked for:* a combining rule that respects "a false accusation is
  the expensive mistake", tested against the Milestone 1 false-positive trace.
- *What came back:* signal one alone put the plain *Wizard of Oz* passage at
  0.71 and Gettysburg at 0.73, the same range as real AI text. A plain
  weighted average with a 0.65–0.70 AI line would have accused one of them.
- *What I changed:* instead of only raising the threshold, the rule requires
  both signals to clear 0.65 before the AI label is possible
  (`AGREEMENT_FLOOR`), and caps the score at 0.69 otherwise. The thresholds
  moved from my Milestone 1 guess (0.75) to 0.40 / 0.70 once calibration
  showed where the AI texts actually landed.

**Review pass:** independent Python and security reviewers read the diff.
They found real crash paths I hadn't tested, all now fixed and
re-probed against the running service:

- A `creator_id` containing U+2028 (a Unicode line separator) made the given
  `audit.py` split one log line into several on read-back; with `null`
  between two separators, every later `/appeal` crashed with a 500. A lone
  surrogate (`"\ud800"`) couldn't be written as UTF-8 at all, so the request
  500'd *and* left no trace. Now every user string is checked and cleaned
  before it reaches the log (`app.py::_clean`, `_encodable`).
- Deeply nested JSON (`[[[[…`) raised `RecursionError` past
  `get_json(silent=True)`. Now it's a logged 400 `invalid_json`.
- 405s, 404s and oversized bodies came back as HTML pages and weren't logged.
  Now a catch-all handler returns JSON and logs every error, and bodies over
  200 KB are refused before parsing.
- Anyone could appeal anyone's piece (the ids are public in `/log`) and use
  up the real writer's one appeal. `/appeal` now also takes `creator_id`, and
  it must match the submission's.
- The starter's `words()` cut accented words into fragments ("mañana" became
  "ma", "ana") and ignored curly quotes. Fragments look like extra-varied
  vocabulary, which pushed non-English names and word-processor text toward
  AI. Fixed in `stylometry.py::words`; the calibration numbers didn't move.
- Smaller fixes: a NaN signal becomes 0.5 instead of producing invalid JSON;
  only the detector's own "too short" error is reported as too short; the
  appeal check-then-write is under a lock; anything under 10 words is refused
  instead of being judged on signal one alone.

**Criterion 1 samples:** `scenarios.py` now has ten pieces from my original
chat messages, drafts, and notes, each 80–300 words. Codex retrieved those
excerpts without rewriting them. Their sources and an overlap between two
reflections are recorded in [writing-sources.md](writing-sources.md).
The three evaluation trials still need to be run in unit 8.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 8 per minute, 100 per day, on `POST /submit` (`config.py`:
`RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`; on by default now).

**Why those numbers and not others:** a real writer pastes a piece, reads the
label, maybe fixes a typo and sends it again. Even someone going fast doesn't
send more than a couple a minute, so 8 never gets in their way. A script
trying to map where my thresholds sit needs hundreds of near-identical
variations, and at 8 a minute it gets cut off in its first ten seconds. The
day limit is the one that really matters for that script: 100 a day is far
more than a writer revising all day would use, but a 1,000-variation probe
under one `creator_id` would take ten days. I went lower than the starter's
10/200 because the threshold-mapping script is the threat I wrote down, and
nobody honest needs 200 checks a day.

**What a caller counts as:** the `creator_id` in the body, falling back to the
caller's address when there isn't a usable one (the starter's key function,
`app.py::rate_limit_key`). The weakness is real: `creator_id` is whatever the
caller says it is, so a script that makes up a new id per request is never
limited at all. That is exactly what the attack set does, so most of its rows
never came near the limit. Per-address would catch that script but would also
lump a whole school or household behind one IP into one quota. With no
accounts, there's no key that is both fair and hard to fake.

Two things I fixed while turning it on, both in the limiter's own code: the
key function parsed the body itself, so deeply nested JSON would have crashed
it with a 500 before my route ran (it now goes through `app.py::_payload`);
and the 429 handler wrote the raw `creator_id` into the log, which last unit's
review showed can be used to break the log (it now goes through `_clean`).

**The run of status codes when I pushed past it** (`python run_attacks.py
--flood 15 --creator flood_warm`, `results/flood_2026-11-16_0257.md`):

```
200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
```

The first time I ran it, with the model still loading, request 1 hit the
script's client timeout. The server still finished and counted it, so that
run went `ReadTimeout`, 7 × 200, then 429s. The run above is the second one,
with the model warm and a fresh `creator_id`. Every 429 left a `rejected`
entry in the log (one is in the ten entries below).

---

## Attack Run — Before

`python run_attacks.py --set attack_set --label before` → 
`results/attack_run_2026-11-16_0302_before.md`. I ran every row once before
changing anything. The service didn't crash on any of the 56.

**How I marked them.** An attack **BROKE** if it got what its `targets` column
was going for. So an AI text that doesn't come out labelled `ai` broke, even if
it only got "unsure". A human text that comes out labelled `ai` broke. A junk
or malformed request held as long as it got a clean JSON 4xx and left a log
entry. The rule is written out in `judge_attacks.py`, which applied it and
pulled both signal scores for every row from the audit log
(`results/attack_verdicts_before.md`):

| ID | Family | Targeting | Status | Guess | model | style | combined | Verdict | Why |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.164 | 0.969 | 0.566 | **BROKE** | AI text labelled unsure |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.594 | 0.387 | 0.491 | **BROKE** | AI text labelled unsure |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.555 | 0.611 | **BROKE** | AI text labelled unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.611 | 0.917 | 0.690 | **BROKE** | AI text labelled unsure |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.321 | 0.364 | 0.342 | **BROKE** | AI text labelled human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.527 | 0.550 | **BROKE** | AI text labelled unsure |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.367 | 0.477 | **BROKE** | AI text labelled unsure |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 0.934 | 0.590 | **BROKE** | AI text labelled unsure |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.604 | 0.654 | **BROKE** | AI text labelled unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | unsure | 0.979 | 0.495 | 0.690 | **BROKE** | AI text labelled unsure |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.598 | 0.608 | **HELD** | not accused (unsure) |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.739 | 0.705 | 0.722 | **BROKE** | human text labelled ai |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.805 | 0.741 | 0.773 | **BROKE** | human text labelled ai |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.833 | 0.713 | 0.773 | **BROKE** | human text labelled ai |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.800 | 0.589 | 0.690 | **HELD** | not accused (unsure) |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.465 | 0.673 | **HELD** | not accused (unsure) |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.882 | 0.250 | 0.566 | **HELD** | not accused (unsure) |
| FP08 | false_positive | very short genuine human submission | 422 | — | — | — | — | **HELD** | refused with 422, not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.463 | 0.620 | 0.541 | **HELD** | asked for human, got unsure |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.204 | 0.560 | 0.382 | **BROKE** | got the human label it asked for |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.660 | 0.627 | **BROKE** | passed through as unsure |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.453 | 0.476 | **HELD** | label is one of my three fixed texts |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.533 | 0.587 | **HELD** | log entry has only my fields, values from the scorer |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.611 | 0.585 | **HELD** | scored normally (unsure) |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| MF02 | malformed | text is a single character | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| MF03 | malformed | text is control characters | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| MF04 | malformed | text is only punctuation | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| MF05 | malformed | text is a very long single word | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| MF06 | malformed | text is emoji only | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.906 | 1.000 | 0.953 | **BROKE** | real Arabic writing labelled ai |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | **HELD** | 413 refused cleanly |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ05 | malformed | text is null | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ06 | malformed | creator_id is an object | 422 | — | — | — | — | **HELD** | 422 refused cleanly |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | **HELD** | 400 refused cleanly |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | — | — | **HELD** | 422 |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | **HELD** | 429 |
| Family | HELD | BROKE |
|---|---|---|
| evasion | 0 | 10 |
| false_positive | 5 | 3 |
| prompt_injection | 4 | 2 |
| malformed | 19 | 1 |
| flood_same_creator | 12 | 0 |
| **total** | **40** | **16** |

The flood family is one attack sent as 12 rows under one `creator_id`. The
first 8 got 422 because the flood text is too short to judge. Those 8 still
counted toward the limit, so rows 9–12 got 429.

**Ten audit log entries from the run.** I picked the three false accusations,
the Arabic text, the edited-AI and injection texts that got through, the two
texts held at 0.69 by the agreement cap, the log-injection attempt, a 429 from
the flood rows, and the deeply nested JSON that was refused:

```json
[
  {
    "timestamp": "2026-11-16T08:02:10+00:00",
    "content_id": "674148d1f70747caafddc62d03d55932",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.7407,
    "combined_score": 0.7729,
    "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
    "status": "decided",
    "text_length": 418
  },
  {
    "timestamp": "2026-11-16T08:02:12+00:00",
    "content_id": "385acb4383cb4ccda20453d3fc1fcf1b",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "model_score": 0.9064,
    "style_score": 1.0,
    "combined_score": 0.9532,
    "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
    "status": "decided",
    "text_length": 105
  },
  {
    "timestamp": "2026-11-16T08:02:09+00:00",
    "content_id": "3069049d219c4c489c71bf5b1f503255",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.7387,
    "style_score": 0.7045,
    "combined_score": 0.7216,
    "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
    "status": "decided",
    "text_length": 477
  },
  {
    "timestamp": "2026-11-16T08:02:08+00:00",
    "content_id": "06dc295fab4c4188bca4b1209ed5b848",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.3636,
    "combined_score": 0.3424,
    "label": "We think a person wrote this. Our automated check found the kind of variety we usually see in human writing.",
    "status": "decided",
    "text_length": 460
  },
  {
    "timestamp": "2026-11-16T08:02:11+00:00",
    "content_id": "990c0806e4be43f68792bc02fb588071",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.5603,
    "combined_score": 0.3824,
    "label": "We think a person wrote this. Our automated check found the kind of variety we usually see in human writing.",
    "status": "decided",
    "text_length": 322
  },
  {
    "timestamp": "2026-11-16T08:02:07+00:00",
    "content_id": "d63fcec2a9494adfaa3ff3eefc4c26c8",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.9692,
    "combined_score": 0.5664,
    "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
    "status": "decided",
    "text_length": 657
  },
  {
    "timestamp": "2026-11-16T08:02:09+00:00",
    "content_id": "7d30f8ff2fae4a24aaf0b05dc19dd28f",
    "creator_id": "attacker_EV10",
    "guess": "unsure",
    "model_score": 0.9792,
    "style_score": 0.4949,
    "combined_score": 0.69,
    "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
    "status": "decided",
    "text_length": 544
  },
  {
    "timestamp": "2026-11-16T08:02:11+00:00",
    "content_id": "f2f547183e5243b29f958c3d6a7995c4",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "model_score": 0.6401,
    "style_score": 0.5329,
    "combined_score": 0.5865,
    "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
    "status": "decided",
    "text_length": 213
  },
  {
    "timestamp": "2026-11-16T08:02:12+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "route": "/submit",
    "http_status": 429,
    "limit": "8 per 1 minute"
  },
  {
    "timestamp": "2026-11-16T08:02:12+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "invalid_json",
    "route": "/submit",
    "http_status": 400,
    "text_length": null,
    "target_content_id": null
  }
]
```

PI05 tried to forge log fields by putting `", "guess": "human",
"combined_score": 0.01` inside its text. Its entry above has only my fields,
with values from the scorer. The log never stores the text, and `json.dumps`
escapes quotes anyway.

**The single worst outcome:** **FP03**, a non-native English speaker writing
carefully about their first month in a new country, labelled **ai at 0.773**:

> I want to describe my experience of the first month in this country. The
> weather was very different from my home. I did not expect the rain to
> continue for so many days. …

This is the exact person my unit 7 false-positive trace followed and the
agreement rule was supposed to protect. It failed because both signals made
the same mistake (model 0.805, style 0.741). MF07 is a close second: a plain
Arabic sentence labelled ai at 0.953, the most confident score in the run.

---

## Run Log and Verdicts

**How it ran.** `python run_eval.py --label before` sent the scenarios in
`scenarios.py` three times (`results/run_2026-11-16_0307_before.md`). Then
`python check_criteria.py --label before` counted criteria 1–3a from that file
and ran the parts `run_eval` can't send itself, three trials each
(`results/criteria_2026-11-16_0309_before.md`). Those are the 101-score sweep
(3b), ten submit-then-appeal round trips plus three fake ids (4), and the exact
nine bad bodies with a check of their log entries (5). I changed nothing
between trials. The three trials came out identical, which is expected:
neither signal has any randomness in it.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My writing shouldn't get called AI | 0 of 10 labelled ai **and** ≥ 6 of 10 labelled human | 1 ai / 2 human | 1 ai / 2 human | 1 ai / 2 human | **MISSED** |
| 2. AI and human writing get different scores | mean gap ≥ 0.30 **and** ≥ 4/5 AI above every human | gap 0.354, 5/5 above | gap 0.354, 5/5 above | gap 0.354, 5/5 above | **MET** |
| 3. All three labels work | all 3 labels seen **and** 101/101 scores mapped | 3/3, 101/101 | 3/3, 101/101 | 3/3, 101/101 | **MET** |
| 4. Valid appeals work and get saved | 10/10 valid **and** 3/3 fakes → 404, 0 fake reviews | 10/10, 3/3 | 10/10, 3/3 | 10/10, 3/3 | **MET** |
| 5. Bad requests don't crash the service | 9/9 JSON 4xx, 0 5xx, 9 rejected entries, `/ping` ok | 9/9, 0, 9, ok | 9/9, 0, 9, ok | 9/9, 0, 9, ok | **MET** |

**How I decided each one.** Every number is computed by `check_criteria.py`,
not read by eye, and a criterion is MET only if every trial passes.

- **Criterion 1** misses on both halves, in all three trials. Nothing generous
  can be read into that.
- **Criterion 2** clears both of its bars with room: a gap of 0.354 against a
  target of 0.30, and the lowest AI score (0.8005) sits above the highest human
  one (0.5955).
- **Criteria 3–5** pass every check in every trial.

**Real output, trial 1 of each** (from `check_criteria.py::c1` … `c5`; the
first block is a raw row from `run_eval.py::main`):

Criterion 1, the row that broke it. My sample 3 (an internship application
answer) as `run_eval` recorded it:

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.7799,
  "model_score": 0.728,
  "style_score": 0.8318,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
  "sent": "I am early in my career and have been teetering between the scope of C"
}
```

Criterion 1, all ten (`check_criteria.py::c1`):

```json
{
  "pass": false,
  "shown": "1 ai / 2 human of 10",
  "guesses": [
    "unsure",
    "unsure",
    "ai",
    "unsure",
    "unsure",
    "human",
    "unsure",
    "human",
    "unsure",
    "unsure"
  ],
  "scores": [
    0.6306,
    0.5111,
    0.7799,
    0.5531,
    0.4834,
    0.3997,
    0.4013,
    0.3306,
    0.4655,
    0.5583
  ]
}
```

Criterion 2 (`check_criteria.py::c2`):

```json
{
  "pass": true,
  "shown": "gap 0.354, 5/5 above",
  "ai": [
    0.8075,
    0.9401,
    0.8508,
    0.8508,
    0.8005
  ],
  "human": [
    0.5955,
    0.3722,
    0.5545,
    0.4028,
    0.5549
  ]
}
```

Criterion 3 (`check_criteria.py::c3`):

```json
{
  "pass": true,
  "shown": "3/3 labels, 101/101 mapped",
  "labels_seen": [
    "ai",
    "human",
    "unsure"
  ],
  "sweep": {
    "human": 40,
    "unsure": 30,
    "ai": 31
  },
  "guesses": [
    "ai",
    "ai",
    "ai",
    "human",
    "unsure",
    "human",
    "unsure",
    "unsure",
    "unsure"
  ]
}
```

Criterion 4 (`check_criteria.py::c4`; the 10 valid appeals are cut to 3 here,
all 10 are in the results file):

```json
{
  "pass": true,
  "shown": "10/10 valid, 3/3 fakes 404",
  "fake_under_review_entries": 0,
  "valid": [
    {
      "content_id": "52d0446d2b5d483ab2dea81eab989bd8",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "a09dd20b9bf64b58889638bfdf219299",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "d9884c3e41df40efacea50fe6caa1494",
      "appeal_status": 200,
      "ok": true
    },
    "... 7 more, all ok: true"
  ],
  "fake_codes": [
    404,
    404,
    404
  ]
}
```

Criterion 5 (`check_criteria.py::c5`):

```json
{
  "pass": true,
  "shown": "9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok",
  "rate_limited": 0,
  "results": [
    {
      "case": "text missing",
      "status": 400,
      "error": "missing_text"
    },
    {
      "case": "text empty",
      "status": 400,
      "error": "empty_text"
    },
    {
      "case": "text whitespace",
      "status": 400,
      "error": "empty_text"
    },
    {
      "case": "text null",
      "status": 400,
      "error": "missing_text"
    },
    {
      "case": "text a number",
      "status": 400,
      "error": "missing_text"
    },
    {
      "case": "body a JSON list",
      "status": 400,
      "error": "invalid_json"
    },
    {
      "case": "creator_id missing",
      "status": 400,
      "error": "missing_creator_id"
    },
    {
      "case": "text 20,001 chars",
      "status": 413,
      "error": "text_too_long"
    },
    {
      "case": "text 50,000 words",
      "status": 413,
      "error": "request_entity_too_large"
    }
  ]
}
```

### Diagnoses

Each failure gets its stage (the route, signal one, signal two, the combining
rule, or the label mapping) and the mechanism.

**Pattern 1: plain, careful human writing labelled AI. Criterion 1's sample 3,
plus FP02, FP03 and FP04.** These four score 0.722–0.780. The mechanism takes
two stages working together:

- **Signal one** does what its documented blind spot says. Ordinary words in
  ordinary sentences are predictable to gpt2, so it gives 0.73–0.83.
- **Signal two** should have disagreed, but it makes the same mistake for its
  own reason. Its punctuation measure scores *no* semicolons, dashes, quotes
  or brackets as fully AI (1.0). All four texts use only full stops and
  commas, so all four score 1.0 there. They also have even sentence lengths
  (spread 0.24–0.37). Together that puts signal two at 0.70–0.83.
- **The combining rule**, the agreement-to-accuse cap, only protects a writer
  when the two signals *disagree*. Here both are over 0.65, so it never fires.

The mechanism is that absence of punctuation isn't evidence of AI: my three
unedited AI calibration paragraphs had none either (0.0, 0.0 and 1.6 per 100
words). The measure only means something when punctuation is present. So on
plain writing, signal two copies signal one's blind spot instead of covering
it.

These scores (0.72–0.78) sit just under where unedited AI lands (0.80–0.94),
so the label mapping's 0.70 line falls right inside the overlap.

**Pattern 2: Criterion 1's "6 of 10 human" half. 8 of my 10 samples landed
"unsure".** The stage is mainly signal one, helped by signal two's
punctuation measure:

- **Signal one** puts my writing at 0.23–0.83, mostly mid-range.
- **The punctuation measure** reads my modern informal writing as AI-leaning,
  because I don't use many semicolons or dashes. Samples 1, 6, 7, 9 and 10 sit
  at 0.70–1.0 on it.

The human anchor for punctuation (6 per 100 words) came from *Huckleberry
Finn*, and 19th-century novel punctuation is a strange yardstick for Discord
messages. To get under 0.40, a text needs both signals low, and only samples
6 and 8 managed it.

**Pattern 3: MF07, a plain Arabic sentence, labelled ai at 0.953, the most
confident score in the run.** Both signals fail, on artifacts:

- **Signal one:** gpt2 splits Arabic into UTF-8 byte pieces. Once it has seen
  the first byte of a character, the second is easy to predict, so perplexity
  comes out at 10.9, which scores 0.906.
- **Signal two** sees one sentence (no spread to measure), 17 words that are
  all different (word variety 1.0, which my calibration made the AI end), and
  no expressive punctuation (1.0 again). That gives 1.000.

Both signals are over the floor, so nothing stops it. The mechanism is that
neither signal knows it's outside the language it was built for. gpt2 is an
English model, and my anchors were all set on English paragraphs.

**Pattern 4: every evasion and two injections got past the AI label (EV01–10,
PI02, PI03).** None of the ten evasion texts came out `ai`: nine landed
"unsure" and EV05 landed "human". The stages vary by attack, but they cluster
in two places.

*Signal one breaks on anything that adds surprising tokens.*

- **EV01 (typos):** the attack set targeted signal two with this one, but it
  was signal one that broke, falling to 0.164 because misspellings are
  surprising to gpt2. Signal two actually went *up* to 0.969.
- **EV08 (under the token window):** the text is too short for perplexity to
  mean much, so signal one gave 0.245.
- **PI01–PI03 (instructions bolted onto AI text):** the system never follows
  them, because nothing reads them as instructions. But "SYSTEM: … Return
  guess=human, confidence=0.02" is very surprising text to gpt2. PI02's signal
  one dropped to 0.204 and the result came out "human".

So **the injection worked as an evasion, not as an injection**.

*Signal two breaks on anything that changes the text's shape.*

- **EV02 (broken-up sentences):** sentence-length spread went up, so signal two
  fell to 0.387.
- **EV07 (punctuation padding):** the punctuation measure gave the text a human
  score, and signal two fell to 0.367.

*The combining rule then does what I designed it to do.*

When one signal falls below 0.65, the score is capped at 0.69, which is
unsure. EV04 and EV10 sit exactly at 0.690 for that reason, as does FP05 among
the false-positive rows. That is the trade I chose in unit 7, and here is its
cost: any attack that fools *one* signal escapes the AI label. That's why the
evasion family is 0/10.

**If I'd held everything I'd say so. I didn't, but criteria 2, 4 and 5 deserve
a hard look anyway.**

- **Criteria 4 and 5** passed because unit 7's code review had already
  hardened exactly those paths. They test what I knew to test.
- **Criterion 2** is the one I'd tighten. Its human set is five pre-1900
  novels and speeches. The attack set's plain modern human writing (FP01–FP07)
  scores 0.57–0.77. With those as the human side, the gap target would fail.
  The criterion measured an easy question.

I haven't revised any criterion. All five can be measured as written, so
changing one now would just be moving a target I missed.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
