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
## 1. My own writing never gets called AI

Of **10 pieces I actually wrote myself** (Discord messages, AI201 discussion
posts, a devlog for one of my Roblox games, a Shorts script I wrote by hand,
notes from my robot-arm build; 80–300 words each, no tool touched them),
**0 get the high-confidence AI label** and **at least 6 of 10 get the
high-confidence human label**. Both have to hold in **every one** of the
three trials.

**Why this target:** I post stuff online. If a site slapped "AI-generated" on
something I wrote, I wouldn't bother appealing, I'd just leave and not come
back. That's the whole reason this project exists, so the number is zero, not
"1 in 10". The 6-of-10 half is there so I can't cheat by calling everything
"unsure". Getting "unsure" on your own work still kind of stings.

---

## 2. Obvious AI and obvious human text land far apart

For **5 clearly-AI texts** (straight out of a chatbot from a plain prompt, no
edits) and **5 clearly-human texts** (published human writing from before
2020), the **average `confidence` of the AI set is at least 0.30 higher** than
the human set's, and **at least 4 of the 5 AI texts score above every one of
the 5 human texts**. Both in each of the three trials.

**Why this target:** if my detector can't split the easy ones, I've got no
business trusting it on the hard ones. 0.30 is exactly how wide my unsure band
is, so with any less, the obvious AI and the obvious human stuff could both
end up stuck in the middle, which is the same as not working.

---

## 3. Every label can actually show up, and every score gets one

(a) In a **9-text coverage set** (3 I'd bet are AI, 3 I'd bet are human, 3 I
honestly can't call), **each of the three labels (`ai`, `human`, `unsure`)
shows up at least once** in each trial.
(b) Running **every score from 0.00 to 1.00 in 0.01 steps (101 values)**
through `scoring.score_to_label` gives back **one of the three guesses for all
101**, with no exception and no gap.

**Why this target:** it's like a game with a level nobody can reach. If a
label never comes out, I wrote it and never tested it. Part (b) is about the
edges: one wrong `<` vs `<=` at a threshold and a score falls through the
crack with no label at all. I'd rather catch that with a loop than with a
confused user.

---

## 4. Appeals always go through, and always leave a record

For **10 appeals against real `content_id`s** (sent with the matching
`creator_id`), **10 of 10** return HTTP 200 with `status: "under_review"`, and
afterwards `GET /log` shows, for each one, the **original decision entry
untouched plus exactly one `appeal` entry** with the writer's reasoning,
timestamped no earlier than the decision. For **3 appeals with made-up
`content_id`s**, **3 of 3 return 404** and **0** `under_review` entries get
added for them.

**Why this target:** the appeal is the only thing a wrongly-flagged person
has. "Works most of the time" isn't good enough when it's the one button they
get, so it's 10 of 10. The fake-id half matters because telling someone "got
it, we're reviewing it" when nothing actually got saved is worse than just
showing an error.

---

## 5. Garbage in doesn't crash it, and always leaves a trace

For **9 malformed requests** (`text` missing, `text` empty, `text` only
whitespace, `text` null, `text` a number, a body that's a JSON list,
`creator_id` missing, `text` of 20,001 characters, and `text` of 50,000
words), **0 return a 5xx**, **9 of 9 return a 4xx with a JSON body that has an
`error` field**, **9 of 9 add exactly one `rejected` entry** to the audit log,
and `POST /ping` still answers afterwards.

**Why this target:** anyone who's played a game on launch day knows the first
thing people do is throw weird stuff at it. A 500 tells the writer nothing
about what to fix, and next unit somebody is literally attacking this thing,
so every refusal has to land in the log. An attack that only shows up as
missing data is one I'd never find.

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
