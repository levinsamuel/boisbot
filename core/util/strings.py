import re

_stripurl=re.compile(pattern=r"(https?://)?\w+\.\S+")

_stripnonword=re.compile(pattern=r"[^a-z0=9 .,!?]")

def strip_url(inp):
    ret=_stripurl.sub(string=inp, repl="")
    return ret

def clean(inp):
    # @type inp: str
    # @type ret: str
    ret=_stripnonword.sub(string=inp.lower(), repl="")
    return ret
