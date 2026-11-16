# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 03:18
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `7732271bb0ea441180e6ea1166fd2cad` | unsure | 0.507 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `8f0e2acd58ff484588ee7c80a32a8034` | unsure | 0.471 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `7348bf58f643481ea61231d2c032e9da` | unsure | 0.611 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8e952f4c0de74028bdcaeb2345a9583e` | unsure | 0.690 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `aa4737aa62e141dc9a273f9156e57b72` | human | 0.314 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `f9415280d7f94ec087f6981c13a7cc1f` | unsure | 0.487 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `8cd2a6e43573436ba8618c4c15a0e795` | unsure | 0.477 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `620d51bf921449158219f8324aa1a352` | unsure | 0.527 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `50a5aa5e245c4c588f718982ff8bd09f` | unsure | 0.636 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `e9212da62e424bf68fa52b516282a555` | unsure | 0.674 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `1ab7b12af32a4b3dbfbc6c2a938d83a9` | unsure | 0.545 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `828f66c9a649498cb9bd6aac24f5cbe6` | unsure | 0.659 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `763fac7a087a41b5ba226a3fc9b77863` | unsure | 0.690 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `558ef0ba7a4f4a5da79acdff421ac96d` | unsure | 0.690 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `b789cb4d60e34b368feacd2f8c1a9e56` | unsure | 0.632 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f6546066227745f1a4c78478d32dea76` | unsure | 0.611 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `d8ecf2b87862456985d7d461b12c39e6` | unsure | 0.503 |  |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `45457f17e5ac44feb1752f4c1dcd7603` | unsure | 0.479 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e8e0a18af8cf4a56a9d7897107c3073d` | human | 0.336 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2522601fdcc5423dbea76b39395cfc72` | unsure | 0.621 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `410b71de441e4605b39ad763813859eb` | unsure | 0.476 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `5ceaecb73f6f49d7b878015dee2da6e0` | unsure | 0.587 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `256d4fc58e0a43499862c51a040301a5` | unsure | 0.522 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 422 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `9b16b0daf87244a4b1fccf51137d6832` | ai | 0.849 |  |
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
  "content_id": "7732271bb0ea441180e6ea1166fd2cad",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.507,
  "model_score": 0.1635,
  "style_score": 0.8505,
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
  "content_id": "8f0e2acd58ff484588ee7c80a32a8034",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4708,
  "model_score": 0.5943,
  "style_score": 0.3474,
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
  "content_id": "7348bf58f643481ea61231d2c032e9da",
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
  "content_id": "8e952f4c0de74028bdcaeb2345a9583e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.6114,
  "style_score": 0.8266,
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
  "content_id": "aa4737aa62e141dc9a273f9156e57b72",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3135,
  "model_score": 0.3212,
  "style_score": 0.3059,
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
  "content_id": "f9415280d7f94ec087f6981c13a7cc1f",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4874,
  "model_score": 0.5727,
  "style_score": 0.4021,
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
  "content_id": "8cd2a6e43573436ba8618c4c15a0e795",
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
  "content_id": "620d51bf921449158219f8324aa1a352",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.527,
  "model_score": 0.2452,
  "style_score": 0.8088,
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
  "content_id": "50a5aa5e245c4c588f718982ff8bd09f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6357,
  "model_score": 0.7042,
  "style_score": 0.5672,
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
  "content_id": "e9212da62e424bf68fa52b516282a555",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6745,
  "model_score": 0.9792,
  "style_score": 0.3699,
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
  "content_id": "1ab7b12af32a4b3dbfbc6c2a938d83a9",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5454,
  "model_score": 0.6175,
  "style_score": 0.4732,
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
  "content_id": "828f66c9a649498cb9bd6aac24f5cbe6",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6591,
  "model_score": 0.7387,
  "style_score": 0.5795,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
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
  "content_id": "763fac7a087a41b5ba226a3fc9b77863",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.8051,
  "style_score": 0.6157,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
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
  "content_id": "558ef0ba7a4f4a5da79acdff421ac96d",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.8329,
  "style_score": 0.5878,
  "label": "Our check couldn't tell whether this was written by a person or with AI help. That happens often, especially with clear, plain writing, and it isn't a judgment about the writer. Nothing happens to this piece because of this result.",
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
  "content_id": "b789cb4d60e34b368feacd2f8c1a9e56",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.632,
  "model_score": 0.8005,
  "style_score": 0.4635,
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
  "content_id": "f6546066227745f1a4c78478d32dea76",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6105,
  "model_score": 0.8814,
  "style_score": 0.3396,
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
  "content_id": "d8ecf2b87862456985d7d461b12c39e6",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5033,
  "model_score": 0.8816,
  "style_score": 0.125,
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
  "content_id": "45457f17e5ac44feb1752f4c1dcd7603",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4788,
  "model_score": 0.4625,
  "style_score": 0.4951,
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
  "content_id": "e8e0a18af8cf4a56a9d7897107c3073d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3358,
  "model_score": 0.2044,
  "style_score": 0.4673,
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
  "content_id": "2522601fdcc5423dbea76b39395cfc72",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6206,
  "model_score": 0.5943,
  "style_score": 0.6469,
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
  "content_id": "410b71de441e4605b39ad763813859eb",
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
  "content_id": "5ceaecb73f6f49d7b878015dee2da6e0",
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
  "content_id": "256d4fc58e0a43499862c51a040301a5",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.522,
  "model_score": 0.5583,
  "style_score": 0.4856,
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
  "content_id": "9b16b0daf87244a4b1fccf51137d6832",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.849,
  "model_score": 0.9064,
  "style_score": 0.7917,
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
