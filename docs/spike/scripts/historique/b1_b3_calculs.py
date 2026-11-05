"""B1/B3 : lit les fichiers Insee, recoupe les séries et calcule les vitesses de vague.
Usage : python -I b1_b3_calculs.py <dossier data/raw/spike/historique>"""
import sys, re, openpyxl, pdfplumber
D = sys.argv[1]
# --- série Insee 2381757 (feuille Figure 1 = immigrés, Figure 2 = étrangers)
wb = openpyxl.load_workbook(f"{D}/insee_2381757.xlsx", data_only=True)
def lire(ws, ncol):
    out = {}
    for r in ws.iter_rows(values_only=True):
        m = re.match(r"^(\d{4})", str(r[0] or ""))
        if m and isinstance(r[1], (int, float)): out[int(m.group(1))] = r[1:ncol]
    return out
imm = lire(wb["Figure 1"], 4)      # effectif, part, pop
etr = lire(wb["Figure 2"], 8)      # FrNais, %, FrAcq, %, Etr, %, pop
print("== Immigrés (2381757)"); 
for y in (1921,1926,1931,1936,1946,1954,1962,1968,1975,1982,1990,1999,2006,2010,2011,2020,2021,2023,2024,2025): print(y, imm.get(y))
def d(y0,y1,s): return round(s[y1][1]-s[y0][1],2)
print("\n== B3 vitesse (points de part d'immigrés)")
print("1921->1931 : +%s pt (%s -> %s)" % (d(1921,1931,imm), imm[1921][1], imm[1931][1]), "| stock +%s k" % round(imm[1931][0]-imm[1921][0]))
for a,b in ((2010,2020),(2011,2021),(2013,2023),(2015,2025)):
    print(f"{a}->{b} : +{d(a,b,imm)} pt ({imm[a][1]} -> {imm[b][1]})", "| stock +%s k" % round(imm[b][0]-imm[a][0]))
print("1962->1975 : +%s pt ; 1946->1954 : +%s pt" % (d(1962,1975,imm), d(1946,1954,imm)))
# --- table croisée lieu de naissance x nationalité (PDF Insee Réf. 2012, fiche 1.2, p.6)
pdf = pdfplumber.open(f"{D}/IMMFRA12_Flot1_pop.pdf")
txt = pdf.pages[5].extract_text()
rows = {}
for l in txt.splitlines():
    l = re.sub(r"^\D+(?=\d{4}\b)", "", l)   # préfixes de mise en page (« France », « métropolitaine »)
    m = re.match(r"^(1911|1921|1926|1931|1936|1946|1954|1962|1968|1975|1982)((?:\s+\d+){8})$", l)
    if m and int(m.group(1)) not in rows: rows[int(m.group(1))] = list(map(int, m.group(2).split()))
print("\n== Table croisée 1911-1982 (milliers) : pop, FrNais(nés FR), FrAcq(nés FR), Etr(nés FR), FrNais(nés étr), FrAcq(nés étr), Etr(nés étr), immigrés")
for y,v in rows.items():
    pop,fn,fa,en,fn2,fa2,en2,im = v
    ok = (abs(fn+fa+en+fn2+fa2+en2-pop)<=3, abs(fa2+en2-im)<=3)   # tolérance d'arrondi
    print(y, v, "somme ok" if all(ok) else f"ECART {ok}", f"| étrangers={en+en2} | immigrés devenus français={100*fa2/max(im,1):.1f} %")
print("Contrôle 1931 étrangers : table", rows[1931][3]+rows[1931][6], "k vs 2381757", etr[1931][4], "k")
print("Contrôle 1962 étrangers : table", rows[1962][3]+rows[1962][6], "k vs 2381757", etr[1962][4], "k")
# --- raccord 1921-1968
print("\n== Raccord : immigrés 2381757 vs table 2012 vs IMMFRA23-F2")
w2 = openpyxl.load_workbook(f"{D}/IMMFRA23-F2.xlsx", data_only=True)["Figure 1"]
f2 = lire(w2, 4)
for y in (1911,1921,1931,1946,1962,1968):
    print(y, "2381757:", imm.get(y,("-",))[0], "| 2023-F2:", f2.get(y,("-",))[0], "| table 2012:", rows.get(y,[0]*8)[7])
