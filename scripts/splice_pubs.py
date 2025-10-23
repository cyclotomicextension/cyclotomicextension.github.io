# scripts/splice_pubs.py
import io, os, re, sys

HTML_SRC = "publications.html"
MARK_START = "<!-- PUBLICATIONS:START -->"
MARK_END   = "<!-- PUBLICATIONS:END -->"

# Prefer Jekyll layout; then your default.html; then index.html; then README.md
CANDIDATES = ["_layouts/default.html", "default.html", "index.html", "README.md"]

def read(path):
    return io.open(path, "r", encoding="utf-8").read()

def write(path, text):
    io.open(path, "w", encoding="utf-8").write(text)

if not os.path.exists(HTML_SRC):
    sys.exit("ERROR: publications.html not found (did the Pandoc step run?)")

html = read(HTML_SRC)
# If Pandoc produced only a list, add a header (optional)
if "<h2" not in html.lower():
    html = "<h2>Publications</h2>\n" + html

target = None
for f in CANDIDATES:
    if os.path.exists(f):
        text = read(f)
        if MARK_START in text and MARK_END in text:
            target = f
            break

if not target:
    sys.exit(
        "ERROR: No markers found.\n"
        "Add markers to one of: _layouts/default.html, default.html, index.html, README.md\n"
        f"{MARK_START}\n(leave empty)\n{MARK_END}\n"
    )

text = read(target)
pat = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), re.S)
rep = f"{MARK_START}\n{html}\n{MARK_END}"
out = pat.sub(rep, text)
write(target, out)
print(f"Updated {target} with publications.")
