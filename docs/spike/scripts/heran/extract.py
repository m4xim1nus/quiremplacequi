import sys, fitz
src, out = sys.argv[1], sys.argv[2]
d = fitz.open(src)
with open(out, "w") as f:
    for i, p in enumerate(d, 1):
        f.write(f"\n=== PAGE {i} ===\n{p.get_text()}")
