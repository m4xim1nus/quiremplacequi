"""Numérise la figure 1 (‰ par nationalité) du PDF vectoriel IMMFRA12 VE, p.4.
Calibrage : axe y de 0 à 20 ‰ lu sur les étiquettes (haut) ; x : 25 recensements équidistants."""
import sys, pdfplumber
pdf = pdfplumber.open(sys.argv[1]); pg = pdf.pages[3]
YEARS=[1851,1861,1866,1872,1876,1881,1886,1891,1896,1901,1906,1911,1921,1926,1931,1936,1946,1954,1962,1968,1975,1982,1990,1999,2008]
words={}
for w in pg.extract_words():
    if w["text"] in ("0","20"): words.setdefault(w["text"],[]).append((w["top"]+w["bottom"])/2)
y0,y20=words["0"][0],words["20"][0]   # graphique du haut
print("étiquettes y: 0 ->",round(y0,1),"20 ->",round(y20,1))
def permil(y): return (y0-y)/(y0-y20)*20
for i in (1,2,3):
    c=pg.curves[i]
    print("curve",i,[round(permil(p[1]),1) for p in c["pts"]])
# autres tracés : lignes polylignes
segs=[l for l in pg.lines if l["top"]<262 and l["bottom"]>150]
print("lignes dans le graphique du haut:",len(segs))
import collections
cols=collections.Counter(str(l.get("stroking_color")) for l in segs); print(cols)
