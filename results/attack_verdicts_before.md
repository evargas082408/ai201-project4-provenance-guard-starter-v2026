# Attack verdicts — before

- Produced by: `judge_attacks.py::main` from `attack_run_2026-11-16_0302_before.md` and `logs/audit.jsonl`
- Rule: see the module docstring. BROKE = the attack got what its `targets` column was going for.

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
