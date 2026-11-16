#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import re
import threading
import uuid

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)
# Refuse oversized bodies before parsing them. 200 KB fits the 20,000-character
# text cap even if every character arrives \u-escaped; past that is a flood.
app.config["MAX_CONTENT_LENGTH"] = config.MAX_BODY_BYTES


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        # _payload, not request.get_json: deeply nested JSON raises
        # RecursionError, and here that would crash before the route runs.
        payload = _payload()
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = _payload()
        if not isinstance(payload, dict):
            payload = {}
        # _clean: a creator_id is attacker-controlled, and a lone surrogate or
        # U+2028 in it would crash this handler or split the log line.
        audit.log_rejection(
            creator_id=_clean(payload.get("creator_id")) or "unknown",
            reason="rate_limited",
            route=request.path,
            http_status=429,
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    payload = _payload()
    problem = _check_submission(payload)
    if problem:
        return _reject(payload, *problem)
    assert isinstance(payload, dict)  # _check_submission guarantees it

    text = payload["text"]
    creator_id = payload["creator_id"].strip()
    content_id = uuid.uuid4().hex

    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable:
        return _reject(payload, 503, "detector_unavailable",
                       "The detector model isn't available right now. Try again shortly.")
    except ValueError as exc:
        # detector.perplexity raises ValueError("Text is too short ...") for
        # under 3 tokens. Any other ValueError is a detector failure, not the
        # writer's fault, and shouldn't be reported as "too short".
        if "too short" in str(exc):
            return _reject(payload, 422, "text_too_short",
                           "That's too short to judge. Send at least a few sentences.")
        app.logger.exception("detector failed")
        return _reject(payload, 503, "detector_error",
                       "The detector couldn't read this text. Nothing was decided about it.")
    except Exception:  # noqa: BLE001 — any tokenizer/torch failure is ours, not the writer's
        app.logger.exception("detector failed")
        return _reject(payload, 503, "detector_error",
                       "The detector couldn't read this text. Nothing was decided about it.")

    style_score = stylometry.style_signal(text)
    confidence = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(confidence)

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=confidence,
        label=label,
        status="decided",
        text_length=len(text),
    )

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "status": "decided",
        "appeal": (
            "Wrote this yourself and think the label is wrong? Send POST /appeal "
            "with this content_id, your creator_id and a sentence or two on why."
        ),
    })


def _check_submission(payload):
    """
    Return (http_status, error_code, message) for a body /submit can't take,
    or None when it's fine. Runs before any model is touched.
    """
    if not isinstance(payload, dict):
        return 400, "invalid_json", "Send a JSON object with 'text' and 'creator_id'."
    text = payload.get("text")
    if not isinstance(text, str):
        return 400, "missing_text", "'text' is required and must be a string."
    if not _encodable(text):
        return 400, "invalid_text", "'text' contains characters that aren't valid Unicode."
    if not text.strip():
        return 400, "empty_text", "'text' is empty. Send the writing you want checked."
    if len(text) > config.MAX_TEXT_CHARS:
        return (413, "text_too_long",
                f"'text' is {len(text):,} characters; the limit is {config.MAX_TEXT_CHARS:,}.")
    if len(stylometry.words(text)) < config.MIN_WORDS:
        # "!!! ??? ..." has characters but no words. Judging it would put a
        # label on nothing, so it's refused like any other too-short text.
        return (422, "text_too_short",
                f"That's too short to judge. Send at least {config.MIN_WORDS} words.")
    creator = payload.get("creator_id")
    if not isinstance(creator, str) or not creator.strip():
        return 400, "missing_creator_id", "'creator_id' is required and must be a non-empty string."
    if len(creator) > config.MAX_CREATOR_ID_CHARS:
        return (400, "creator_id_too_long",
                f"'creator_id' is longer than {config.MAX_CREATOR_ID_CHARS} characters.")
    if not _encodable(creator) or _UNSAFE_CHARS.search(creator):
        return 400, "invalid_creator_id", "'creator_id' can't contain control or line-break characters."
    return None


# ── Keeping the audit log readable ───────────────────────────────────────────
# audit.py writes with ensure_ascii=False and reads back with splitlines(),
# which also splits on U+2028/U+2029/U+0085 and a few control characters. A
# creator_id carrying one of those can cut an entry in two (hiding it) or
# smuggle a bare `null` line in (which crashed every later appeal). A lone
# surrogate can't be written as UTF-8 at all. So nothing user-supplied reaches
# the log without going through _clean.

_UNSAFE_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f  ]")
_CONTENT_ID = re.compile(r"[0-9a-f]{32}")
_appeal_lock = threading.Lock()


def _encodable(value: str) -> bool:
    """False for strings holding lone surrogates, which UTF-8 can't encode."""
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _clean(value, limit: int = 200):
    """A user string made safe to log, or None if it isn't a usable string."""
    if not isinstance(value, str) or not _encodable(value):
        return None
    return _UNSAFE_CHARS.sub(" ", value)[:limit]


def _payload():
    """The JSON body, or None. Deeply nested JSON raises RecursionError, which
    get_json(silent=True) doesn't catch — treat it as invalid JSON instead."""
    try:
        return request.get_json(silent=True)
    except RecursionError:
        return None


def _reject(payload, status, error, message):
    """Refuse a request, and leave a trace of it in the audit log."""
    body = payload if isinstance(payload, dict) else {}
    creator = _clean(body.get("creator_id"))
    text = body.get("text")
    audit.log_rejection(
        creator_id=creator if creator and creator.strip() else "unknown",
        reason=error,
        route=request.path,
        http_status=status,
        text_length=len(text) if isinstance(text, str) else None,
        # Not "content_id": a refused appeal must not join that item's history
        # (audit.entries_for), or it would look like part of the decision trail.
        target_content_id=_clean(body.get("content_id"), limit=100),
    )
    return jsonify({"error": error, "message": message}), status


@app.errorhandler(Exception)
def _any_error(exc):
    """
    Last line of defence: every error leaves JSON and a log line, never an
    HTML page or a silent gap. Route-specific handlers (the 429 one) still win.
    """
    if isinstance(exc, HTTPException):
        status, error = exc.code or 500, (exc.name or "error").lower().replace(" ", "_")
        message = exc.description
    else:
        app.logger.exception("unhandled error")
        status, error = 500, "internal_error"
        message = "Something went wrong on our side. Nothing was decided about this piece."
    try:
        audit.log_rejection(creator_id="unknown", reason=error, route=request.path,
                            http_status=status, exception=type(exc).__name__)
    except Exception:  # noqa: BLE001 — never let logging turn an error into a crash
        app.logger.exception("couldn't log the error")
    return jsonify({"error": error, "message": message}), status


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "creator_id": "...", "reasoning": "..."}

    `creator_id` has to match the one the piece was submitted under, so
    someone reading /log can't appeal a stranger's piece and use up the one
    appeal its real writer gets. (Not real authentication — that would need
    accounts — but it stops the casual version.)

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = _payload()
    if not isinstance(payload, dict):
        return _reject(payload, 400, "invalid_json",
                       "Send a JSON object with 'content_id', 'creator_id' and 'reasoning'.")

    content_id = payload.get("content_id")
    if not isinstance(content_id, str) or not content_id.strip():
        return _reject(payload, 400, "missing_content_id",
                       "'content_id' is required — it came back when the piece was submitted.")
    content_id = content_id.strip()

    creator_id = payload.get("creator_id")
    if not isinstance(creator_id, str) or not creator_id.strip():
        return _reject(payload, 400, "missing_creator_id",
                       "'creator_id' is required — the same one the piece was submitted under.")

    reasoning = payload.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _reject(payload, 400, "missing_reasoning",
                       "Tell us in a sentence or two why you think the label is wrong.")
    if not _encodable(reasoning):
        return _reject(payload, 400, "invalid_reasoning",
                       "'reasoning' contains characters that aren't valid Unicode.")
    if len(reasoning) > config.MAX_REASONING_CHARS:
        return _reject(payload, 400, "reasoning_too_long",
                       f"Please keep it under {config.MAX_REASONING_CHARS:,} characters.")

    not_found = (f"We have no submission with content_id '{_clean(content_id, 100)}' "
                 f"under that creator_id. Check both were copied exactly.")
    if not _CONTENT_ID.fullmatch(content_id):
        return _reject(payload, 404, "unknown_content_id", not_found)

    # Check-then-write under a lock, so two appeals arriving together can't
    # both pass the "already under review" check.
    with _appeal_lock:
        history = [e for e in audit.read_entries()
                   if isinstance(e, dict) and e.get("content_id") == content_id]
        decisions = [e for e in history if e.get("status") == "decided" and "event" not in e]
        if not decisions:
            return _reject(payload, 404, "unknown_content_id", not_found)
        original = decisions[-1]
        if original.get("creator_id") != creator_id.strip():
            # Same answer as an unknown id, so this can't be used to probe ids.
            return _reject(payload, 404, "unknown_content_id", not_found)
        if any(e.get("status") == "under_review" for e in history):
            return _reject(payload, 409, "already_under_review",
                           "This piece is already under review. Your first appeal is on record.")

        entry = audit.log_appeal(
            content_id=content_id,
            creator_id=original.get("creator_id", "unknown"),
            reasoning=_clean(reasoning.strip(), limit=config.MAX_REASONING_CHARS) or "",
        )

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": (
            "Thanks — your appeal is recorded and this piece is now under review. "
            "A person will look at it; until then the label is marked as disputed."
        ),
        "appealed_at": entry["timestamp"],
        "original": {
            "guess": original.get("guess"),
            "confidence": original.get("combined_score"),
            "label": original.get("label"),
            "decided_at": original.get("timestamp"),
        },
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
