# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is never called AI

Of **10 pieces I wrote myself** (class discussion posts, emails, notes, a short
story paragraph; 80–300 words each, unedited by any tool), **0 are labelled
high-confidence AI**, and **at least 6 of 10 are labelled high-confidence
human**. Both have to hold in **each** of the three trials.

**Why this target:** On a writing site, labelling a real person's work as AI is
the mistake that drives them off the site, so I allow none, not one in ten.
The "6 of 10 human" half is there so that I can't meet the first half just by
calling everything unsure. An unsure label on someone's real work is still a
cost to them, only a smaller one.

---

## 2. Clearly-AI and clearly-human text land far apart

For **5 clearly-AI texts** (chatbot output from a plain prompt, pasted
unedited) and **5 clearly-human texts** (published, pre-2020 human prose),
the **mean `confidence` of the AI set is at least 0.30 higher** than the mean
of the human set, and **at least 4 of the 5 AI texts score above every one of
the 5 human texts**. Both in each of three trials.

**Why this target:** If the obvious cases don't separate by a wide margin,
nothing the label says can be trusted on the hard cases. 0.30 is the width of
my unsure band, so a smaller gap would mean the obvious AI and obvious human
texts could both sit inside "unsure".

---

## 3. Every label is reachable, and every score maps to exactly one

(a) In a **9-text coverage set** (3 I expect to be AI, 3 I expect to be human,
3 I judge borderline), **each of the three labels (`ai`, `human`, `unsure`)
is returned at least once** in each trial.
(b) Feeding every score from **0.00 to 1.00 in 0.01 steps (101 values)** to
`scoring.score_to_label` returns **one of the three guesses for all 101**,
with no exception and no gap.

**Why this target:** A label that can never be produced is one I wrote and
never tested. Part (b) checks the boundaries themselves, because an
off-by-one between `<` and `<=` at a threshold is how a score ends up with no
label at all.

---

## 4. An appeal always changes status and is always recorded

For **10 appeals against real `content_id`s**, **10 of 10** return HTTP 200 with
`status: "under_review"`, and afterwards `GET /log` shows, for each one, the
**original decision entry unchanged plus exactly one `appeal` entry** with the
writer's reasoning, timestamped no earlier than the decision. For **3 appeals
with made-up `content_id`s**, **3 of 3 return 404** and **0** `under_review`
entries are added for them.

**Why this target:** The appeal is the only thing between a wrong accusation
and nothing at all, so "usually works" isn't good enough; it has to be 10 of
10. The 404 half matters because an appeal that "succeeds" against a typo'd id
tells the writer they were heard when nothing was recorded.

---

## 5. Bad input is refused cleanly and leaves a trace

For **9 malformed requests** — `text` missing, `text` empty, `text` only
whitespace, `text` null, `text` a number, a body that is a JSON list,
`creator_id` missing, `text` of 20,001 characters, and `text` of 50,000 words —
**0 return a 5xx**, **9 of 9 return a 4xx with a JSON body containing an
`error` field**, **9 of 9 add exactly one `rejected` entry** to the audit log,
and `POST /ping` still answers afterwards.

**Why this target:** A crash on malformed input is one of the most common real
failures, and a 500 tells a writer nothing about what to fix. Logging every
refusal matters because unit 8 is about attacks, and an attack that shows up
only as an absence is one I would never find.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
