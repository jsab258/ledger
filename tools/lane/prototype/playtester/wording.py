"""Does a prompt's wording fit the person it is about? Pure functions, no browser.

A prompt such as "Talk to the old woman at the window opposite" or "Speak to a man" names a
person by a description. These checks compare the description's words with the person's own
record (sex, age, whether Tom knows the name). Written by the cloud lane, 18 Nov 2026.
"""
import re

FEMALE = {"woman", "women", "lady", "landlady", "housekeeper", "girl", "she", "her", "widow", "mrs", "wife", "mother", "nun"}
MALE = {"man", "men", "lad", "lads", "boy", "he", "him", "his", "priest", "father", "mr", "husband", "watchman", "fella", "chap", "bloke"}
OLD = {"old", "elderly", "aged"}
YOUNG = {"young", "lad", "girl", "boy", "kid", "youth"}

OLD_FROM = 60      # "old" fits from about this age (a plain reading, not a rule of the game)
YOUNG_UNTIL = 35   # "young" or "lad" fits up to about this age


def words(text):
    return set(re.findall(r"[a-z]+", (text or "").lower()))


def label_of(prompt_text):
    """The person part of a talk prompt: 'Talk to the priest' -> 'the priest'."""
    m = re.match(r"^(?:Talk to|Speak to)\s+(.*)$", prompt_text or "")
    return m.group(1) if m else None


def wording_faults(label, sex=None, age=None, name=None, name_known=None):
    """Faults of a label against one person's record, as plain sentences (empty list: fits)."""
    w = words(label)
    out = []
    if sex == "m" and w & FEMALE and not (w & MALE):
        out.append("calls a man %r" % label)
    if sex == "f" and w & MALE and not (w & FEMALE):
        out.append("calls a woman %r" % label)
    if age is not None:
        if w & OLD and age < OLD_FROM:
            out.append("says old for someone aged %s" % age)
        if w & YOUNG and age > YOUNG_UNTIL:
            out.append("says young or lad for someone aged %s" % age)
    if name and name_known is False:
        parts = [p for p in re.findall(r"[A-Za-z']+", name) if p not in ("Father", "Mrs", "Mr", "the", "The")]
        if any(re.search(r"\b%s\b" % re.escape(p), label or "") for p in parts if len(p) > 2):
            out.append("shows the name %r before Tom has learned it" % name)
    return out


def classify_reply(text, person_id, stock):
    """'own' (this person's written line), 'stock' (a line anyone may say), or 'other' (neither list:
    a line made by the game from what the person knows, a scene line or a model line)."""
    t = (text or "").strip()
    if t in set(stock.get("own", {}).get(person_id, [])):
        return "own"
    if t in set(stock.get("keeperBarks", {}).get(person_id, [])):
        return "own"
    if t in set(stock.get("generic", [])):
        return "stock"
    return "other"
