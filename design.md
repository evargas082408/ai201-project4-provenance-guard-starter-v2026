# Milestone 1 — tracing a submission before building one

Written before any route code existed. The README's *What This Does* section is
the cleaned-up version of this.

## 1. The path a piece of text takes

1. **The route (`app.py::submit`).** A writing site sends `POST /submit` with
   JSON `{"text", "creator_id"}`. The route checks the body before anything
   else: it has to be a JSON object, `text` a non-empty string under the size
   cap, and `creator_id` a non-empty string. A bad body is refused here with a
   400/413 and logged as a rejection, so it never reaches a model.
   *Adds:* a `content_id` (uuid) that every later step and the appeal hang off.
2. **Signal one (`detector.py::model_signal`).** gpt2, running locally, reads
   the text and reports how predictable it found it (perplexity → 0–1).
   *Adds:* `model_score`.
3. **Signal two (`stylometry.py::style_signal`).** Measures the text's shape
   without reading it: sentence-length spread, vocabulary variety,
   expressive punctuation. *Adds:* `style_score`.
4. **The combining rule (`scoring.py::combine_signals`).** Two numbers become
   one. Weighted average, plus a rule that the system may only *accuse* when
   both signals lean AI. *Adds:* `confidence` (the combined 0–1 score).
5. **The label mapping (`scoring.py::score_to_label`).** The number becomes one
   of three sentences a reader can understand. *Adds:* `guess` and `label`.
6. **The audit log (`audit.py::log_decision`).** One JSON line in
   `logs/audit.jsonl` with the timestamp, ids, both signal scores, the combined
   score, the guess, the label and `status: "decided"`.
7. **The response.** The writer (and the site) get back all of the above, plus
   a line telling them how to appeal.
8. **The appeal (`app.py::appeal`), later.** The writer sends the `content_id`
   and their reasons. The route checks the id exists, appends an `appeal` entry
   with `status: "under_review"` next to the original decision, and confirms.

## 2. The two signals and their blind spots

**Signal one: model predictability (gpt2 perplexity).**
- *Measures:* how easy the text is for a language model to predict, word by word.
- *Why it differs:* a model writes by picking likely next words, so model text
  is text a model finds predictable. People make odder choices.
- *Blind spot:* predictability is not authorship. Plain, common-word writing
  (second-language writers, young writers, anyone writing simply) is as
  predictable as machine text, so it gets scored as AI. The reverse also
  fails: AI text prompted to use rare, ornate words looks "surprising" and
  scores human. It only sees the first 400 tokens.

**Signal two: stylometry (the shape of the text).**
- *Measures:* sentence-length variation, moving-average type-token ratio, and
  expressive punctuation per 100 words.
- *Why it differs:* generated prose marches in even, mid-length sentences with
  tidy punctuation; human writing is lumpy, with fragments, asides, dashes,
  contractions.
- *Blind spot:* it cannot read. Anything that changes the shape without the
  substance moves it: splitting or merging sentences, adding typos, sprinkling
  in dashes and exclamation marks, pasting a quotation. A careful human writer
  with very even sentences (a lot of formal or technical writing) looks AI to
  it. On very short text it has almost nothing to measure.

They measure different things: one is a model's view of word *choice*, the
other is a count of *structure*. They can disagree, which is the useful part.

## 3. Tracing the false positive

A student who learned English as a second language writes a short, plain
paragraph about their weekend. Short sentences, common words, few commas.

- **Signal one** finds it very predictable: model score around 0.85.
- **Signal two** sees fairly even sentences and little punctuation: maybe 0.6.
- With a plain weighted average that is ~0.75 — high-confidence AI. That is
  the accusation this project exists to avoid.

What I want instead:
- The high-confidence AI label needs a **high bar** (≥ 0.75 combined) **and
  agreement** (both signals ≥ 0.60 on their own). If either signal is not
  clearly on the AI side, the score is capped just under the AI line and the
  text lands in *unsure*.
- The *unsure* label must not read as an accusation. It says we can't tell,
  that this is common for plain writing, and that nothing happens to the
  writer because of it.
- **Every** label, including the AI one, carries the appeal route and the
  `content_id`. The appeal moves the piece to `under_review` and is logged
  next to the original decision, so a reviewer sees both.

Who pays: AI text written to look plain will more often land in *unsure*
rather than *AI*. I accept that; a missed detection costs the site a little,
a wrong accusation costs a person a lot.

## 4. The contract

### `POST /submit`

Request:

| field | type | rule |
|---|---|---|
| `text` | string | required; not blank after trimming; at most 20,000 characters |
| `creator_id` | string | required; not blank; at most 200 characters |

Success `200`:

| field | type | meaning |
|---|---|---|
| `content_id` | string | uuid hex; what `/appeal` takes |
| `creator_id` | string | echoed back |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | float 0–1 | combined score; 0 = confidently human, 1 = confidently AI |
| `label` | string | the full sentence a reader sees |
| `model_score` | float 0–1 | signal one on its own (higher = more AI) |
| `style_score` | float 0–1 | signal two on its own (higher = more AI) |
| `status` | string | `"decided"` |
| `appeal` | string | how to contest the label |

Errors (all JSON `{"error": <code>, "message": <sentence>}`, all logged as
rejections):

| status | `error` | when |
|---|---|---|
| 400 | `invalid_json` | body isn't a JSON object |
| 400 | `missing_text` | `text` absent or not a string |
| 400 | `empty_text` | `text` is blank |
| 400 | `missing_creator_id` | `creator_id` absent, not a string, blank or too long |
| 413 | `text_too_long` | over 20,000 characters |
| 422 | `text_too_short` | too short for the model to score |
| 503 | `detector_unavailable` | the model couldn't load |

### `POST /appeal`

Request:

| field | type | rule |
|---|---|---|
| `content_id` | string | required; must exist in the log |
| `reasoning` | string | required; not blank; at most 5,000 characters |

Success `200`: `{"content_id", "status": "under_review", "message",
"appealed_at", "original": {"guess", "confidence", "label"}}`.

Errors: `400 invalid_json` / `missing_content_id` / `missing_reasoning` /
`reasoning_too_long`; `404 unknown_content_id` when no decision has that id;
`409 already_under_review` when the item is already under review (the first
appeal is kept; the duplicate is refused rather than silently stacked).
