import re

stripurl=re.compile(pattern=r"(https?://)?\w+\.\S+")

stripnonword=re.compile(pattern=r"\b\S*?\W\S*?\b")