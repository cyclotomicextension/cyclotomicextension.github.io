# scripts/splice_pubs.py
import io, os, re, sys

README = "README.md"
HTML   = "publications.html"
START  = "<!-- PUBLICATIONS:START -->"
END    = "<!-- PUBLICATIONS:END -->"

if not os.path.exists(README):
    sys.exit("ERROR: README.md not found")
if not os.path.exists(HTML):
    sys.exit("ERROR: publications.html not found")

readme = io.open(README, "r", encoding="utf-8").read()
html   = io.open(HTML, "r", encoding="utf-8").read()

# If Pandoc produced a bare list, add a header so it’s obvious
if "<h2" not in html.lower():
    html = "<h2>Publications</h2>\n" + html

pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
replacement = f"{START}\n{html}\n{END}"

if pattern.search(readme):
    out = pattern.sub(replacement, readme)
else:
    out = readme.rstrip() + "\n\n" + replacement + "\n"

io.open(README, "w", encoding="utf-8").write(out)
print("README.md updated.")
