"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import math

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. ← TODO (Milestone 4)

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    ⚠️ **Write the rule down before you code it, and put the numbers in your
    README.** A weighted average is the obvious choice and it is not the only
    one. Things worth thinking about:

      - **What happens when they disagree?** One signal at 0.9 and the other at
        0.1 averages to 0.5 — "unsure". Is that what you want? It might be
        exactly right: two methods disagreeing IS uncertainty. Or you might
        decide one signal is more trustworthy when they split.

      - **Which way do you want to be wrong?** Weighting toward the signal that
        reads more human means fewer false accusations and more AI text
        getting through. There's no weighting that avoids the trade.

      - Milestone 4 asks you to find a case where your two signals split and
        write it down. That case is what this rule exists to handle.

    The weights in config.py are placeholders. Change them, or ignore them and
    write a different rule.
    """
    # My rule, written down before it was coded (README "Signals and Scoring"):
    #
    #   1. Weighted average: 0.5 × model + 0.5 × style. Neither signal is
    #      trustworthy enough on its own to outvote the other; each has a blind
    #      spot the other partly covers.
    #   2. Agreement to accuse: if EITHER signal on its own is below
    #      AGREEMENT_FLOOR, the score is capped just under AI_THRESHOLD. Two
    #      methods disagreeing is uncertainty, and uncertainty must never come
    #      out as "this is AI". The cap only works in the accusing direction —
    #      being wrongly called human is the cheap mistake, so no cap there.
    # A NaN would slip past both the clamp and the cap below (every
    # comparison with NaN is False) and come out as invalid JSON. Treat any
    # non-finite signal as "no evidence": 0.5, which can never clear the
    # agreement floor, so it can never help produce an accusation.
    model_score = _finite_or_neutral(model_score)
    style_score = _finite_or_neutral(style_score)

    combined = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    ) / (config.WEIGHT_MODEL_SIGNAL + config.WEIGHT_STYLE_SIGNAL)

    if min(model_score, style_score) < config.AGREEMENT_FLOOR:
        combined = min(combined, config.AI_THRESHOLD - 0.01)

    return round(combined, 4)


def _finite_or_neutral(value) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.5
    if not math.isfinite(value):
        return 0.5
    return min(max(value, 0.0), 1.0)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    # Half-open bands, so every score lands in exactly one:
    #   [0, HUMAN)  human  ·  [HUMAN, AI)  unsure  ·  [AI, 1]  ai
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score < config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


# The exact text a reader sees. Written for someone who has never heard the
# word "threshold" — and, for the unsure and AI ones, for the writer who may
# well have written every word.

LABEL_HUMAN = (
    "We think a person wrote this. Our automated check found the kind of "
    "variety we usually see in human writing."
)

LABEL_UNSURE = (
    "Our check couldn't tell whether this was written by a person or with AI "
    "help. That happens often, especially with clear, plain writing, and it "
    "isn't a judgment about the writer. Nothing happens to this piece because "
    "of this result."
)

LABEL_AI = (
    "Our check found strong signs that this may have been written with AI. "
    "Automated checks can be wrong, so this is not proof. If you wrote this "
    "yourself, you can ask for a review and a person will look at it."
)


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – under {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – under {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]


if __name__ == "__main__":
    # Print the bands, and prove every score from 0.00 to 1.00 gets a label
    # (criterion 3b).
    for name, band in label_ranges():
        print(f"{name:24} {band}")
    seen = {}
    for i in range(101):
        guess, _ = score_to_label(i / 100)
        seen.setdefault(guess, []).append(i / 100)
    for guess, scores in seen.items():
        print(f"{guess:8} {len(scores):3} scores  {scores[0]:.2f} … {scores[-1]:.2f}")
    print(f"total    {sum(len(s) for s in seen.values())} of 101 mapped")
