"""Inspecte les tracés vectoriels d'une page (figure 1 : ‰ par nationalité)."""
import sys, pdfplumber
pg = pdfplumber.open(sys.argv[1]).pages[int(sys.argv[2]) - 1]
for i, c in enumerate(pg.curves):
    pts = c["pts"]
    print(i, c.get("stroking_color"), c.get("non_stroking_color"), len(pts), [tuple(round(v,1) for v in p) for p in pts[:3]])
for w in pg.extract_words():
    if w["text"] in ("0","4","8","12","16","20","1851","2008","1931"): print(w["text"], round(w["x0"],1), round(w["top"],1))
