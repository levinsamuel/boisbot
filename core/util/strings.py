import re

_stripurl=re.compile(pattern=r"(https?://)?\w+\.\S+")

_stripnonword=re.compile(pattern=r"\b\S*?\W\S*?\b")

def strip_url(inp):
    ret=_stripurl.sub(string=inp, repl="")
    return ret

def strip_nonword(inp):
    ret=_stripnonword.sub(string=inp, repl="")
    return ret