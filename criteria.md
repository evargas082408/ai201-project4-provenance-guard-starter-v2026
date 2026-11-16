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
## 1. My writing shouldn't get called AI

Of **10 pieces I actually wrote myself** (original chat messages, essay
drafts, class reflections, programming explanations, and robotics notes;
80–300 words each, with no AI rewriting in the test samples),
**0 get the high-confidence AI label** and **at least 6 of 10 get the
high-confidence human label**. Both have to hold in **every one** of the
three trials.

**Why this target:** If I wrote something myself, I don't want it getting
called AI. That's why I picked zero false positives. At least 6 of 10 also
need to get the human label so it can't pass by calling everything unsure.

---

## 2. AI and human writing should get different scores

For **5 clearly-AI texts** (straight out of a chatbot from a plain prompt, no
edits) and **5 clearly-human texts** (published human writing from before
2020), the **average `confidence` of the AI set is at least 0.30 higher** than
the human set's, and **at least 4 of the 5 AI texts score above every one of
the 5 human texts**. Both in each of the three trials.

**Why this target:** I want to check whether it can tell the easier examples
apart before trusting it with anything harder. I picked 0.30 because that's
the width of the unsure band. I also want most AI examples to score above
every human example, so one high score can't carry the average.

---

## 3. All three labels should work

(a) In a **9-text coverage set** (3 I'd bet are AI, 3 I'd bet are human, 3 I
honestly can't call), **each of the three labels (`ai`, `human`, `unsure`)
shows up at least once** in each trial.
(b) Running **every score from 0.00 to 1.00 in 0.01 steps (101 values)**
through `scoring.score_to_label` gives back **one of the three guesses for all
101**, with no exception and no gap.

**Why this target:** Having three labels doesn't mean much if the system
only ever uses two. I also want to check every score in 0.01 steps so a
mistake at a cutoff doesn't leave a score without a label.

---

## 4. Valid appeals should work and get saved

For **10 appeals against real `content_id`s** (sent with the matching
`creator_id`), **10 of 10** return HTTP 200 with `status: "under_review"`, and
afterwards `GET /log` shows, for each one, the **original decision entry
untouched plus exactly one `appeal` entry** with the writer's reasoning,
timestamped no earlier than the decision. For **3 appeals with made-up
`content_id`s**, **3 of 3 return 404** and **0** `under_review` entries get
added for them.

**Why this target:** If the system gets someone's writing wrong, they need
to be able to appeal it. All 10 valid appeals should work and leave a record
of what happened. A made-up ID should get an error instead of saying an
appeal went through when there's nothing to review.

---

## 5. Bad requests shouldn't crash the service

For **9 malformed requests** (`text` missing, `text` empty, `text` only
whitespace, `text` null, `text` a number, a body that's a JSON list,
`creator_id` missing, `text` of 20,001 characters, and `text` of 50,000
words), **0 return a 5xx**, **9 of 9 return a 4xx with a JSON body that has an
`error` field**, **9 of 9 add exactly one `rejected` entry** to the audit log,
and `POST /ping` still answers afterwards.

**Why this target:** People will send empty text, the wrong type of data,
or way too much text. I want those requests to get an error without crashing
the service. All 9 need to show up in the log so I can see what was rejected
when I test attacks in unit 8.

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
