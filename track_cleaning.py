import re

QUALIFIER = (
    r'(?:'
    r'(?:\d{4}\s*)?'  # optional year
    r'(?:remaster(?:ed)?(?: version)?|remix|mix|extended(?: mix| version)?|'
    r'radio edit|single(?: version)?|edit|live(?: at [^\]\)\}]*?)?|'
    r'acoustic(?: version)?|demo|instrumental|mono(?: version)?|'
    r'stereo(?: mix| version)?|version|original mix|club mix|bonus track|'
    r'deluxe(?: version)?)'
    r')'
)

PATTERNS = [
    re.compile(rf'\s*[-–—]\s*{QUALIFIER}\s*$', re.I),
    re.compile(rf'\s*[\(\[\{{]\s*{QUALIFIER}[^\)\]\}}]*[\)\]\}}]\s*$', re.I),
]

def clean_title(title: str) -> str:
    t = title.strip()
    while True:
        prev = t
        for p in PATTERNS:
            t = p.sub('', t)
        t = re.sub(r'\s*[-–—:]+\s*$', '', t).strip()
        if t == prev:
            return t
