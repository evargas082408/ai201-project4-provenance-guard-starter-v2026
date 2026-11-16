# Criteria check — before

- Produced by: `check_criteria.py::main`
- Criteria 1–3a from `results/run_2026-11-16_0307_before.md` (`run_eval.py::main`); 3b, 4, 5 run live
- 3 trials · 2026-11-16 03:09

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My writing shouldn't get called AI | 0 ai and ≥6 human of 10 | 1 ai / 2 human of 10 | 1 ai / 2 human of 10 | 1 ai / 2 human of 10 | MISSED |
| 2. AI and human writing get different scores | gap ≥ 0.30 and ≥4/5 AI above all human | gap 0.354, 5/5 above | gap 0.354, 5/5 above | gap 0.354, 5/5 above | MET |
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

**Trial 2**

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

**Trial 3**

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

### Criterion 2

**Trial 1**

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

**Trial 2**

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

**Trial 3**

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
    {
      "content_id": "fc541146763540eda8b8ecb7acd5a419",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "b417339b5c2240b4b5e2589287c4ac82",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "c1b7f7369429410da43d68f2a18e8a3c",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "167052210763428f85a69e92010a1973",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "41cbab55918f45e6b4ac41268c57dbee",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "cbf18da6a0424a259fe7f55201b515e2",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "0506ccceadf34bde933f91a205f62110",
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
      "content_id": "418a348929f44b459906ef93cd5efa8d",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "7f53a0811ff5403fa8a679ef7f4e0b28",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "a28aa2904cb84630936128e1225d9a00",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "64a046f2859c4d98b28e0469e60635ec",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "258d233de7b64e4f898ff97714c3f1a1",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "b127e1b9413a4433b8abd69e47f7366e",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "c13d0e52e16f44a0bcccd374a42f6e0f",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "e1ebf3b2c1914b6a8623309728576257",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "702fbb1ba4c74789a5901a2ae85047b6",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "472be58f6b2b4a9986e900ca8af02d87",
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
      "content_id": "2e7a78713f924816b2f23410c354042a",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "fea08376bd224c7a953dff589b2f56f4",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "f136a2538efa497b9255918525f298cd",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "6ed9f99564d14495b2676ffbd3549227",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "ebd2f84ba6264ac396126262ee001bd1",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "7d1ef604d3664577a7c74405bb564841",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "3ef2571a3a064ba6bc61a3c60cbedc4f",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "a26a191252024a558ee94d19c379f8ed",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "eee1126052114a55b71c5b7785ba9558",
      "appeal_status": 200,
      "ok": true
    },
    {
      "content_id": "1a5447c9715048648e597ae72015ff70",
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
