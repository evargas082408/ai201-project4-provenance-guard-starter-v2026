# Criteria check — after

- Produced by: `check_criteria.py::main`
- Criteria 1–3a from `results/run_2026-11-16_0318_after.md` (`run_eval.py::main`); 3b, 4, 5 run live
- 3 trials · 2026-11-16 03:20

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My writing shouldn't get called AI | 0 ai and ≥6 human of 10 | 1 ai / 3 human of 10 | 1 ai / 3 human of 10 | 1 ai / 3 human of 10 | MISSED |
| 2. AI and human writing get different scores | gap ≥ 0.30 and ≥4/5 AI above all human | gap 0.346, 5/5 above | gap 0.346, 5/5 above | gap 0.346, 5/5 above | MET |
| 3. All three labels work | 3/3 labels seen, 101/101 scores mapped | 3/3 labels, 101/101 mapped | 3/3 labels, 101/101 mapped | 3/3 labels, 101/101 mapped | MET |
| 4. Valid appeals work and get saved | 10/10 valid, 3/3 fakes 404, 0 fake reviews | 10/10 valid, 3/3 fakes 404 | 10/10 valid, 3/3 fakes 404 | 10/10 valid, 3/3 fakes 404 | MET |
| 5. Bad requests don't crash the service | 9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok | 9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok | 9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok | 9/9 JSON 4xx, 0 5xx, 9 rejected logged, ping ok | MET |

---

## Per-trial detail

### Criterion 1

**Trial 1**

```json
{
  "pass": false,
  "shown": "1 ai / 3 human of 10",
  "guesses": [
    "unsure",
    "unsure",
    "ai",
    "unsure",
    "unsure",
    "human",
    "human",
    "human",
    "unsure",
    "unsure"
  ],
  "scores": [
    0.5829,
    0.4846,
    0.7174,
    0.5531,
    0.4592,
    0.3487,
    0.3478,
    0.3306,
    0.4173,
    0.4958
  ]
}
```

**Trial 2**

```json
{
  "pass": false,
  "shown": "1 ai / 3 human of 10",
  "guesses": [
    "unsure",
    "unsure",
    "ai",
    "unsure",
    "unsure",
    "human",
    "human",
    "human",
    "unsure",
    "unsure"
  ],
  "scores": [
    0.5829,
    0.4846,
    0.7174,
    0.5531,
    0.4592,
    0.3487,
    0.3478,
    0.3306,
    0.4173,
    0.4958
  ]
}
```

**Trial 3**

```json
{
  "pass": false,
  "shown": "1 ai / 3 human of 10",
  "guesses": [
    "unsure",
    "unsure",
    "ai",
    "unsure",
    "unsure",
    "human",
    "human",
    "human",
    "unsure",
    "unsure"
  ],
  "scores": [
    0.5829,
    0.4846,
    0.7174,
    0.5531,
    0.4592,
    0.3487,
    0.3478,
    0.3306,
    0.4173,
    0.4958
  ]
}
```

### Criterion 2

**Trial 1**

```json
{
  "pass": true,
  "shown": "gap 0.346, 5/5 above",
  "ai": [
    0.756,
    0.8776,
    0.7958,
    0.7883,
    0.7714
  ],
  "human": [
    0.533,
    0.3408,
    0.492,
    0.4028,
    0.4924
  ]
}
```

**Trial 2**

```json
{
  "pass": true,
  "shown": "gap 0.346, 5/5 above",
  "ai": [
    0.756,
    0.8776,
    0.7958,
    0.7883,
    0.7714
  ],
  "human": [
    0.533,
    0.3408,
    0.492,
    0.4028,
    0.4924
  ]
}
```

**Trial 3**

```json
{
  "pass": true,
  "shown": "gap 0.346, 5/5 above",
  "ai": [
    0.756,
    0.8776,
    0.7958,
    0.7883,
    0.7714
  ],
  "human": [
    0.533,
    0.3408,
    0.492,
    0.4028,
    0.4924
  ]
}
```

### Criterion 3

**Trial 1**

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

**Trial 2**

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

**Trial 3**

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

### Criterion 4

**Trial 1**

```json
{
  "pass": true,
  "shown": "10/10 valid, 3/3 fakes 404",
  "fake_under_review_entries": 0,
  "valid": [
    {
      "content_id": "27d53ef11eca42ce8df02fc86a597624",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "4a44ecf40860409a9facd326dde1ff9f",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "906453e87c4a48438b6b6572326d210d",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "105ac42c37434543b4235e685d820365",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "12539947bb6c4dd7815cc029d0bebbb0",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "4e3e94600f8d46bdb16db1d7b55eb8ef",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "8a26fe9d1a664789a193de3867a03820",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "b31bdcc2d0da46a394444d3bda275d82",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "be4f28dc5fa64b50ba1a1d2ecf5e8354",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "70cdb8dd994c41e4bd06656ec09f2a27",
      "appeal_status": 200,
      "ok": true
    }
  ],
  "fake_codes": [
    404,
    404,
    404
  ]
}
```

**Trial 2**

```json
{
  "pass": true,
  "shown": "10/10 valid, 3/3 fakes 404",
  "fake_under_review_entries": 0,
  "valid": [
    {
      "content_id": "52d13cd9dc154e1f815ad9aa6f8c6ae3",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "b99a5f82f33f4b0fb3b98ee9ebc35c85",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "63fcac9a71714b4b87dcde639ef7371d",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "41bfa6739db54344858950386d628c24",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "682b6f4e2b684be2be6aad7069884f26",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "2180a5691df8461ea0be28e508ee7730",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "70436535a15945eba423e10d78fc3d36",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "7de2046eb9474ece845924af620eb5a7",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "47d000f6139f419483d09224ae86a43f",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "d749f245653344d08454e715ccb0f2ec",
      "appeal_status": 200,
      "ok": true
    }
  ],
  "fake_codes": [
    404,
    404,
    404
  ]
}
```

**Trial 3**

```json
{
  "pass": true,
  "shown": "10/10 valid, 3/3 fakes 404",
  "fake_under_review_entries": 0,
  "valid": [
    {
      "content_id": "bba7fae39f364227b0dba1a535d109b7",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "c570b53884e24c22ac58308c64fff5e3",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "56bdc712d2614e779df1a972e2aaf51c",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "d0cacdcc3bc94eeca4cc1a0a9f5eec68",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "69ec61b9b23b473fb05c833c8ff52349",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "362b320de13e4fbcaff5486ab1b805c1",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "0309270da7d64bac94125dd70f2b92f7",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "a39ac8bf7a304985892ec4c34bdca930",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "17a9455aa06e47a6a1df25c16c30e739",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "0f6f1fa651df43ca931774c5857a8858",
      "appeal_status": 200,
      "ok": true
    }
  ],
  "fake_codes": [
    404,
    404,
    404
  ]
}
```

### Criterion 5

**Trial 1**

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

**Trial 2**

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

**Trial 3**

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
