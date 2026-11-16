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

**Still mine to do:** criterion 1 is about *my own* writing. None of the text
above is mine (the human samples are public-domain books), so before unit 8
I need to put ten pieces I actually wrote into `scenarios.py`.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



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
