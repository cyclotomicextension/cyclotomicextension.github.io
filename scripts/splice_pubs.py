# scripts/splice_pubs.py
import io, os, re, sys

HTML_SRC = "publications.html"
MARK_START = "<!-- PUBLICATIONS:START -->"
MARK_END   = "<!-- PUBLICATIONS:END -->"

# Prefer index.html (your homepage), then README.md
CANDIDATES = ["index.html", "README.md"]

def load(path):
    return io.open(path, "r", encoding="utf-8").read()

def save(path, text):
    io.open(path, "w", encoding="utf-8").write(text)

if not os.path.exists(HTML_SRC):
    sys.exit("ERROR: publications.html not found. Did the Pandoc step run?")

html = load(HTML_SRC)
# Add a header if Pandoc produced only a list
if "<h2" not in html.lower():
    html = "<h2>Publications</h2>\n" + html

target = None
for f in CANDIDATES:
    if os.path.exists(f):
        text = load(f)
        if MARK_START in text and MARK_END in text:
            target = f
            break

if not target:
    sys.exit(
        "ERROR: No markers found.\n"
        "Add these markers either to index.html or README.md:\n"
        f"{MARK_START}\n(leave empty)\n{MARK_END}\n"
    )

text = load(target)
pat = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), re.S)
rep = f"{MARK_START}\n{html}\n{MARK_END}"
out = pat.sub(rep, text)
save(target, out)
print(f"Updated {target} with {len(html)} chars of publications.")
