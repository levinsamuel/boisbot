import re

_stripurl = re.compile(pattern=r"https?://\w+\.\S+")

_cr = re.compile(pattern=r"\r")
_lf = re.compile(pattern=r"\n")
_word_seps = re.compile(pattern=r"[\n\r_\-]")

_stripnonsentence = re.compile(pattern=r"[^a-z0-9 \-().,'!?_]")
_stripnonword = re.compile(pattern=r"[^a-z _]")


def strip_url(inp):
    ret = _stripurl.sub(string=inp, repl="")
    return ret


def clean(inp, strip_non_word=False, strip_urls=False):
    """Clean an input strings

Options:
    strip_non_word: If true, remove all characters that are not words.
Otherwise, remove all characters that are not typical in a sentence, leaving
other characters like numbers and punctuation"""

    # @type inp: str
    # @type ret: str
    lwr = inp.lower()
    if strip_urls:
        lwr = strip_url(lwr)
    ret = _normalize_word_separators(lwr)
    pat = _stripnonword if strip_non_word else _stripnonsentence
    ret = pat.sub(string=ret, repl="")
    return ret


def _normalize_word_separators(inp):

    return _word_seps.sub(string=inp, repl=" ")
