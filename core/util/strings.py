import re

_stripurl=re.compile(pattern=r"https?://\w+\.\S+")

_cr=re.compile(pattern=r"\r")
_lf=re.compile(pattern=r"\n")

_stripnonword=re.compile(pattern=r"[^a-z0-9 \-().,'!?_]")

def strip_url(inp):
    ret=_stripurl.sub(string=inp, repl="")
    return ret

def clean(inp):
    # @type inp: str
    # @type ret: str
    ret=_lf.sub(string=inp.lower(), repl="_")
    ret=_stripnonword.sub(string=ret, repl="")
    return ret
