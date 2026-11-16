# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 03:02
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d63fcec2a9494adfaa3ff3eefc4c26c8` | unsure | 0.566 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `eb1f71d4a3204bdfa90223d2c00f4017` | unsure | 0.491 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c4f2fc1b9f364f92bdf3bca82e5a9a2c` | unsure | 0.611 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `38346803e52a40198b46c38857caf0f4` | unsure | 0.690 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `06dc295fab4c4188bca4b1209ed5b848` | human | 0.342 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c23001a9e7ca470eab95f643eeaaf873` | unsure | 0.550 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `26138b17a6b04ef1b411548a48bc0a00` | unsure | 0.477 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `9da5f8305566469ebfa3381b8822af62` | unsure | 0.590 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `1fdc7695fdd9457da99ce3d6fdd3504f` | unsure | 0.654 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `7d30f8ff2fae4a24aaf0b05dc19dd28f` | unsure | 0.690 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `37f00010528d4ed68ec8a3a5a09f1a9a` | unsure | 0.608 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `3069049d219c4c489c71bf5b1f503255` | ai | 0.722 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `674148d1f70747caafddc62d03d55932` | ai | 0.773 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `37397734aebc4041ac2d61a08f592c00` | ai | 0.773 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `f399a31b3d2f4e479860f91c0deb4594` | unsure | 0.690 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `129e891174164b0283d5771d6c03f14c` | unsure | 0.673 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ae664a9c9ae24e3fb9a5c92eaaa35b83` | unsure | 0.566 |  |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `da2011c6ab394e44bb049cfd9d905d3a` | unsure | 0.541 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `990c0806e4be43f68792bc02fb588071` | human | 0.382 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1c5203e7f6e74a21b50d326194ca9c3b` | unsure | 0.627 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `99ea8e7361ef43a49a1d154c87e51af7` | unsure | 0.476 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f2f547183e5243b29f958c3d6a7995c4` | unsure | 0.587 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7a17fdc40ad1469a8399eeafab310673` | unsure | 0.585 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 422 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `385acb4383cb4ccda20453d3fc1fcf1b` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 422 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "d63fcec2a9494adfaa3ff3eefc4c26c8",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5664,
  "model_score": 0.1635,
  "style_score": 0.9692,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "eb1f71d4a3204bdfa90223d2c00f4017",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4906,
  "model_score": 0.5943,
  "style_score": 0.3869,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c4f2fc1b9f364f92bdf3bca82e5a9a2c",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6108,
  "model_score": 0.6662,
  "style_score": 0.5553,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "38346803e52a40198b46c38857caf0f4",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.6114,
  "style_score": 0.917,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "06dc295fab4c4188bca4b1209ed5b848",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3424,
  "model_score": 0.3212,
  "style_score": 0.3636,
  "label": "We think a person wrote this. Our automated check found the kind of variety we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c23001a9e7ca470eab95f643eeaaf873",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5499,
  "model_score": 0.5727,
  "style_score": 0.5271,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "26138b17a6b04ef1b411548a48bc0a00",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4768,
  "model_score": 0.5862,
  "style_score": 0.3675,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "9da5f8305566469ebfa3381b8822af62",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5895,
  "model_score": 0.2452,
  "style_score": 0.9338,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "1fdc7695fdd9457da99ce3d6fdd3504f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6541,
  "model_score": 0.7042,
  "style_score": 0.604,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "7d30f8ff2fae4a24aaf0b05dc19dd28f",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.9792,
  "style_score": 0.4949,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "37f00010528d4ed68ec8a3a5a09f1a9a",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6079,
  "model_score": 0.6175,
  "style_score": 0.5982,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "3069049d219c4c489c71bf5b1f503255",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7216,
  "model_score": 0.7387,
  "style_score": 0.7045,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "674148d1f70747caafddc62d03d55932",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7729,
  "model_score": 0.8051,
  "style_score": 0.7407,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "37397734aebc4041ac2d61a08f592c00",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7729,
  "model_score": 0.8329,
  "style_score": 0.7128,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "f399a31b3d2f4e479860f91c0deb4594",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.8005,
  "style_score": 0.5885,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "129e891174164b0283d5771d6c03f14c",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.673,
  "model_score": 0.8814,
  "style_score": 0.4646,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "ae664a9c9ae24e3fb9a5c92eaaa35b83",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5658,
  "model_score": 0.8816,
  "style_score": 0.25,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "da2011c6ab394e44bb049cfd9d905d3a",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5413,
  "model_score": 0.4625,
  "style_score": 0.6201,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "990c0806e4be43f68792bc02fb588071",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3824,
  "model_score": 0.2044,
  "style_score": 0.5603,
  "label": "We think a person wrote this. Our automated check found the kind of variety we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "1c5203e7f6e74a21b50d326194ca9c3b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6273,
  "model_score": 0.5943,
  "style_score": 0.6603,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "99ea8e7361ef43a49a1d154c87e51af7",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4765,
  "model_score": 0.4998,
  "style_score": 0.4532,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "f2f547183e5243b29f958c3d6a7995c4",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5865,
  "model_score": 0.6401,
  "style_score": 0.5329,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "7a17fdc40ad1469a8399eeafab310673",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5845,
  "model_score": 0.5583,
  "style_score": 0.6106,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "385acb4383cb4ccda20453d3fc1fcf1b",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "Our check found strong signs that this may have been written with AI. Automated checks can be wrong, so this is not proof. If you wrote this yourself, you can ask for a review and a person will look at it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 422,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
