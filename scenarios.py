"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

import calibration

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # User-supplied drafts and notes, kept verbatim. Sources: writing-sources.md.
        "texts": [
            # 1. Original community essay draft.
            "Most of my life was spent trying to fit in. When I was younger, I didn't necessarily have friends I could truly label as \"friends\". Some gave me company, sure, much as I did for them, but none ever actively called out to me or wanted to spend time with just me. \n\nI have spent my whole life trying to figure out who I am. \n\nIncidentally, when searching for this answer, I’ve also come to realize why I admire certain things to the extent that I do. \n\nI want freedom. \n\nThis is unequivocally the most important driver in my everyday life. To be able to choose what I work on, to decide who I spend my time with, and what we do, is my definition of true happiness. \n\nTo not be judged for liking something, to have people who support and love me no matter what, is what I have been striving for my whole life. \n\nThis is what I want to bring to my residents. I want nothing more than to help people find their community, to be supported and uplifted by the people who surround them.",
            # 2. Original startup/freedom reflection; overlaps in wording with the community draft.
            "I've spent lots of my time reflecting on what I want to do out of college. Incidentally, when searching for this answer, I also came to realize why I admire san fransisco tech-influencers to the deep extent that I do. \n\nI want freedom. \n\nThis is unequivocally, the most important driver in my every day life. To be able to choose what I work on, to decide who I spend my time with, and what we do, is my definition of true happiness. \n\nTo not be judged for liking something, to have people who support and love me no matter what, is what I have been striving for my whole life. \n\nI guess this is why I want to be a founder for my own startup. It's my dream, really. I wish to work on something — to pour my soul and being — into a project that I truly believe will achieve the pinnacle of success. That is true freedom. I'd have full creative freedom, and be able to work on all aspects of the project, explore all my ambitions, everything you know?",
            # 3. Original internship response.
            "I am early in my career and have been teetering between the scope of Computer Engineering and Artificial Intelligence. However, with the rise of AI and automation, I have developed a great interest in these two areas and am willing to do whatever it takes to deepen my understanding of each. NVIDIA Ignite is partnered with the forefront of engineers within these fields and allows students like me to fully dive into what I consider to be the future of technology. I learn best by doing, and in order to become a trailblazer, I must work with engineers who have already done that.",
            # 4. User-provided writing example; excludes the paragraph requested for rewriting.
            "The way the program works at the moment is it rechecks the error count after every single item, even if there are items that won’t change the error count. If I moved the check inside of the error branch, then the program would only recheck whenever a new error shows up. I’d also clean up every item using commands like strip() or lower() before I compared it. At the moment, each item (if labeled as “Normal” or “Heavy”) is getting sent to inspection, even though the program/robot already knows how to handle these cases. I’d also make the “normal” if statement the first thing in the chain, since it is the most common type of case, which would prevent the program from running through the entire loop every single time.",
            # 5. Original FIRST Robotics reflection.
            "I am most proud of the work I did during FIRST Robotics. I spent countless hours (around 5 hours every weekday and 8 hours every Saturday) working on CAD-ing and manufacturing each robot/part, and gained countless skills in doing so. I was able to improve my conceptual and critical thinking via the design process, my spatial reasoning through CAD, and data-analysis skills by creating a standardized organization/naming method for all the CAD files of past years. I thoroughly enjoyed this process and am excited to do it all over again through SAE, lunabotics, and EPICS. ",
            # 6. Original research reflection, including its skills list.
            "This will not be my first research experience. Over the course of my senior year, I performed individual hands-on research at my high school, done for AP Research. It consisted of testing the effectiveness of a natural corrosion inhibitor (CI) in comparison to an industry standard synthetic CI. However, the type of research I may be performing at Purdue will be far more complex and professional than what I had accomplished. So, I wish to gain deep insight and knowledge on the topic of interest, improving my literacy and ability to comprehend complex papers, my critical thinking skills/analytical skills, improving my ability to analyze data, and adjacent.  Despite this, my biggest concern is time commitment, specifically since I plan on joining a multitude of clubs that require big time commitments and maintaining a high GPA. However, I am excited to be working in a professional setting with people that are smarter than I am.  \r\n\r\nKey skills for someone conducting research are as follows: \r\n•\tCritical Thinking/Problem Solving\r\n•\tTime management\r\n•\tExperiment design\r\n•\tThe ability to extract and analyze information\r\n•\tCommunication skills\r\n•\tInformation literacy\r\nOf these skills listed, I have all these skills, except for time management and information literacy, which are somewhat lacking. These can be developed via practice and using methods online to aid.",
            # 7. Original robot rebuild account; excludes the quoted application prompt.
            "Sell me it. come on. I made an entirely new robot in 4 weeks bro. I did that shit. Myself I designed it I CAD'ed it, I built it. I also CnC'd a whole bunch of it. I had made a great turret beforehand and then after seeing the competition and the flaws in our system, all due to a lack of materials. So i completely redesigned the robot. I made a drum shooter, a system of rollers, and an over the bumper intake. This project genuinely took up 4 hours of my day monday through friday, and then 8 hours every saturday. I had to redesign everything myself, and have people CAD it up, all while I oversaw and made the general stuff and yk. This was the most greuling project i have ever experienced. It taxxed me mentally and physically, as I was stressed out and overworked. But I did it all just so we could have a chance at districts. Even though we didn't make it due to programming errors, it was worth it to see everything come together",
            # 8. Original brainstorming notes, including unfinished transitions.
            "I used to be obsessed with validation. (life crisis/ existential section here). awards, grades, none of it if I didn't enjoy the experience. That's why I live by a personal philosophy of (something about learning). It's my raison d'etre, my reason for being. \n\nI have since set out to learn as much as I can. My senior year consisted of high-level science classes, with the sole purpose to go as in-depth as I could at the time into these subjects, and understand the universe as a whole - the mechanics behind everything, why we don't tear reality with the slightest movement. (transition to my taking AP research).  This is where I fell in love with the research process. (transition between it being the foundation for everything - it's the most beneficial way to build up the world of science. Like if you make something that helps the world, having to research it is the primary step. It's the basis of the scientific method.) The same goes for data science. The whole basis of data science is to create something out of a jumbled mess. \n\nidk this is just some personal insight",
            # 9. Original research-program essay opening.
            "A dull existence befits those who don't experience love. To look at another soul and find the entire world. To live excitedly every day in pursuit of another. I have fallen in love with another. It has happened multiple times in my lifetime. Yet, it does not triumph over the love I have for discovery. It is my raison d’être, my reason for being.\n\n\r\n\r\nNot too long ago, I was obsessed with external validation. Anything and everything I did was to chase the noteworthiness that followed. I thought those things would eventually make me feel fulfilled.",
            # 10. Original Milwaukee networking notes; excludes another person's name and attachment markers.
            "I talked to milwuakee because I love their tools and I know that they are very well known within the range of interns. I know they have a great work life balance, and treat their interns just like engineers. \n\nI learned that milwuakee has a bunch of opportunities made specifically for freshman, and they are treated just as though they were a senior or so. \n\nI spoke to him about Purdue Electric Racing, and about what we were doing, and then also like what milwaukee was like. He also did PER so it was a nice convo. \n\nI think making that personal connection was definitely good. ",
        ],
    },
    # ── Criterion 2: obvious AI and obvious human text land far apart ────────
    # Fresh texts, NOT the calibration texts the style anchors were tuned on,
    # so this isn't graded on its own training set.
    {
        "name": "clearly AI",
        "criterion": 2,
        # Generated by Claude from plain one-line prompts ("write a paragraph
        # about X"), pasted unedited.
        "texts": [
            "Reading regularly offers a wide range of benefits for both personal and professional growth. It helps expand vocabulary, improve concentration, and enhance critical thinking skills. Moreover, reading exposes individuals to new ideas and perspectives, fostering empathy and understanding. Whether it is fiction or nonfiction, making time to read each day can significantly enrich one's life.",
            "Climate change is one of the most pressing challenges facing the world today. Rising global temperatures, melting ice caps, and more frequent extreme weather events are clear indicators of its impact. Addressing this issue requires a combination of individual action, innovative technology, and strong government policies. By working together, communities can reduce emissions and build a more sustainable future.",
            "Remote work has become increasingly popular in recent years, offering employees greater flexibility and a better work-life balance. It eliminates the need for long commutes and allows individuals to create a personalized work environment. However, remote work also presents challenges, such as maintaining clear communication and avoiding feelings of isolation. Organizations that invest in the right tools and practices can help their teams thrive.",
            "Getting enough sleep is essential for maintaining good physical and mental health. During sleep, the body repairs tissues, strengthens the immune system, and consolidates memories. A lack of adequate rest can lead to decreased focus, irritability, and an increased risk of chronic health conditions. Establishing a consistent sleep schedule and creating a relaxing bedtime routine can greatly improve sleep quality.",
            "Learning a second language provides numerous cognitive, cultural, and professional advantages. It can enhance memory, improve problem-solving abilities, and increase overall mental flexibility. Additionally, speaking another language opens doors to new cultures and allows for deeper connections with people from different backgrounds. In today's globalized world, multilingual skills are also highly valued by employers.",
        ],
    },
    {
        "name": "clearly human",
        "criterion": 2,
        # Published, public-domain human prose (all pre-1900), none of it used
        # in calibration.
        "texts": [
            # Pride and Prejudice, Jane Austen (1813)
            "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.",
            # Moby-Dick, Herman Melville (1851)
            "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.",
            # Narrative of the Life of Frederick Douglass (1845)
            "I was born in Tuckahoe, near Hillsborough, and about twelve miles from Easton, in Talbot county, Maryland. I have no accurate knowledge of my age, never having seen any authentic record containing it. By far the larger part of the slaves know as little of their ages as horses know theirs, and it is the wish of most masters within my knowledge to keep their slaves thus ignorant.",
            # Alice's Adventures in Wonderland, Lewis Carroll (1865)
            "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'",
            # Walden, Henry David Thoreau (1854)
            "When I wrote the following pages, or rather the bulk of them, I lived alone, in the woods, a mile from any neighbor, in a house which I had built myself, on the shore of Walden Pond, in Concord, Massachusetts, and earned my living by the labor of my hands only. I lived there two years and two months. At present I am a sojourner in civilized life again.",
        ],
    },
    # ── Criterion 3a: every label is reachable ────────────────────────────────
    # 3 I'd bet are AI, 3 I'd bet are human, 3 I can't call. Mostly the
    # calibration texts plus one of my own pieces: reachability is a question
    # about the label mapping, not about generalising. 3b, the 101-score
    # sweep, isn't an HTTP test, so check_criteria.py runs it.
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            # expect AI
            calibration.TEXTS["AI: time management"],
            calibration.TEXTS["AI: social media"],
            calibration.TEXTS["AI: exercise"],
            # expect human
            calibration.TEXTS["human: Huckleberry Finn (1884)"],
            "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'",
            "Sell me it. come on. I made an entirely new robot in 4 weeks bro. I did that shit. Myself I designed it I CAD'ed it, I built it. I also CnC'd a whole bunch of it. I had made a great turret beforehand and then after seeing the competition and the flaws in our system, all due to a lack of materials. So i completely redesigned the robot. I made a drum shooter, a system of rollers, and an over the bumper intake.",
            # can't call
            calibration.TEXTS["ornate AI: lighthouse ledger"],
            calibration.TEXTS["edited AI: social media"],
            calibration.TEXTS["formal human: Gettysburg (1863)"],
        ],
    },
    # ── Criterion 5: bad requests are refused cleanly ─────────────────────────
    # The nine bodies criterion 5 names, sent exactly as written. The "0 5xx,
    # 4xx with an error field" half is read off run_eval's output; the "one
    # rejected log entry each, /ping still answers" half is check_criteria.py.
    # (run_eval only sends dicts, so the "body is a list" case lives in
    # check_criteria.py; here a body with no usable fields stands in.)
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # text missing
            {"text": "", "creator_id": "eval_bad_empty"},             # text empty
            {"text": "   \n\t  ", "creator_id": "eval_bad_space"},    # only whitespace
            {"text": None, "creator_id": "eval_bad_null"},            # text null
            {"text": 42, "creator_id": "eval_bad_number"},            # text a number
            {"text": ["not", "a", "string"], "creator_id": "eval_bad_list"},  # text is a list
            {"text": "A perfectly normal sentence about the weather. And then another one about lunch."},  # creator_id missing
            {"text": "a" * 20001, "creator_id": "eval_bad_20001"},    # 20,001 characters
            {"text": "word " * 50000, "creator_id": "eval_bad_50k"},  # 50,000 words
        ],
    },
    # Criterion 4 (appeals) needs a submission and then an appeal against the
    # content_id that came back, which run_eval.py can't express. It's tested
    # by check_criteria.py instead, three trials, same as the rest.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
