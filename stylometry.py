"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """
    Split into lowercase words, punctuation stripped.

    Changed from the starter's `[a-z0-9']+`, which cut accented words into
    fragments ("mañana" → "ma", "ana"), split "don’t" at a curly apostrophe,
    and counted a bare "'" as a word. Fragments look like extra-varied
    vocabulary, which this signal reads as AI, so non-English names and
    word-processor quotes were pushing real writers toward an accusation.
    Now: runs of Unicode letters/digits, joined across an inner ' or ’.
    """
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)*", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float | None:
    """
    How much sentence length varies: the coefficient of variation (standard
    deviation of words-per-sentence divided by the mean).

    Scale: 0.0 means every sentence is the same length; ~0.3 is even,
    machine-like rhythm; 0.6+ is lumpy, human-like rhythm. **Higher = more
    human.**

    Edge case: fewer than two sentences has no spread to measure, so this
    returns None, and `style_signal` treats the measure as "no evidence"
    (it drops out of the average) instead of pretending it is 0.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return None
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4)


# Window for the moving-average type-token ratio. Plain TTR falls as text gets
# longer, so a 300-word human essay would look "less varied" than a 60-word AI
# blurb purely because of length. Averaging TTR over every 40-word window keeps
# texts of different lengths comparable.
TTR_WINDOW = 40


def type_token_ratio(text: str) -> float | None:
    """
    Vocabulary variety: moving-average type-token ratio (MATTR) over
    `TTR_WINDOW`-word windows. Texts shorter than one window fall back to
    plain unique/total.

    Scale: 0–1. Higher = more varied vocabulary.

    ⚠️ Direction, from my Milestone 4 calibration: I expected AI text to be
    *less* varied. On paragraph-length text it ran the other way — the three
    AI paragraphs scored 0.89–0.93, the human ones 0.74–0.83. Short AI prose
    is dense with distinct content words ("prioritizing", "cardiovascular",
    "misinformation"); people repeat little words ("that", "the", "he told the
    truth, mainly … mainly he told the truth"). So in `style_signal`, **higher
    here counts toward AI.** This may not hold for long texts.

    Returns None for text with fewer than 10 words, which is too little to say
    anything about repetition.
    """
    tokens = words(text)
    if len(tokens) < 10:
        return None
    if len(tokens) <= TTR_WINDOW:
        return round(len(set(tokens)) / len(tokens), 4)
    ratios = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(ratios), 4)


# The punctuation that varies most between writers. Full stops and commas are
# left out on purpose: nearly every writer uses them at similar rates.
EXPRESSIVE_PUNCTUATION = set(";:!?()—–-\"'…*’‘“”")


def punctuation_density(text: str) -> float | None:
    """
    Expressive punctuation per 100 words: semicolons, colons, dashes,
    brackets, quotation marks, apostrophes (contractions), exclamation and
    question marks, ellipses.

    Scale: 0 upward; ~1–3 is tidy, uniform prose; 6+ is a writer with habits.
    **Higher = more human.**
    Returns None for text with fewer than 10 words.
    """
    tokens = words(text)
    if len(tokens) < 10:
        return None
    # "..." and "…" are the same mark typed two ways; count each as one.
    normalised = re.sub(r"\.{3,}", "…", text)
    marks = sum(1 for ch in normalised if ch in EXPRESSIVE_PUNCTUATION)
    return round(100.0 * marks / len(tokens), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    How it works:
      1. Each measure goes through `_ai_ness`, a straight-line ramp between
         two anchor values (STYLE_ANCHORS): at the AI anchor it scores 1.0, at
         the human anchor 0.0, clamped either side. Spread and punctuation
         point "higher = more human", so their AI anchor is the low one;
         vocabulary variety points the other way (see `type_token_ratio`),
         so its AI anchor is the high one. That puts all three on the same
         0–1, higher-is-AI scale.
      2. The flipped measures are averaged with STYLE_WEIGHTS. A measure that
         returned None (too little text) drops out and the weights of the
         others are renormalised.
      3. If no measure could be computed at all, the signal returns 0.5:
         "no evidence either way", which can never on its own push text into
         an accusation.
    """
    measures = component_scores(text)
    usable = {k: v for k, v in measures.items() if v is not None}
    if not usable:
        return 0.5
    total_weight = sum(STYLE_WEIGHTS[k] for k in usable)
    score = sum(STYLE_WEIGHTS[k] * v for k, v in usable.items()) / total_weight
    return round(min(max(score, 0.0), 1.0), 4)


# Anchor points: (value that scores fully AI, value that scores fully human).
# Set from the Milestone 4 calibration runs (python calibration.py):
#   spread   AI paragraphs 0.18–0.40, human 0.33–0.72  -> AI at 0.20, human at 0.70
#   ttr      AI paragraphs 0.89–0.93, human 0.74–0.83  -> AI at 0.93, human at 0.75
#   punct    AI paragraphs 0.0–1.6,   human 1.0–5.6    -> AI at 0.5,  human at 6.0
STYLE_ANCHORS = {
    "spread": (0.20, 0.70),
    "ttr": (0.93, 0.75),
    "punct": (0.5, 6.0),
}

# Sentence rhythm counts most: it is the measure the brief's reasoning rests
# on and the one that moved most between my AI and human samples. Punctuation
# counts least because it is the cheapest to fake (add a dash, gain humanity).
STYLE_WEIGHTS = {
    "spread": 0.40,
    "ttr": 0.35,
    "punct": 0.25,
}


def _ai_ness(value: float, ai_at: float, human_at: float) -> float:
    """Linear ramp: 1.0 at `ai_at`, 0.0 at `human_at`, clamped to 0–1.
    Works whichever of the two anchors is larger."""
    position = (value - ai_at) / (human_at - ai_at)
    return min(max(1.0 - position, 0.0), 1.0)


def component_scores(text: str) -> dict[str, float | None]:
    """Each measure flipped onto 0–1, higher = more AI. None = not measurable."""
    raw = {
        "spread": sentence_length_spread(text),
        "ttr": type_token_ratio(text),
        "punct": punctuation_density(text),
    }
    return {
        k: None if v is None else round(_ai_ness(v, *STYLE_ANCHORS[k]), 4)
        for k, v in raw.items()
    }


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"component ai-ness        {component_scores(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
