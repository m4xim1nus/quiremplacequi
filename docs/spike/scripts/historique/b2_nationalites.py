"""B2 : part des nationalités dans la population (IP 1910, encadré) -> ordre de grandeur des stocks,
recoupé avec les valeurs ponctuelles lues dans des sources secondaires (Mourlane 2016, MNHI Polonia)."""
import sys, openpyxl
D = sys.argv[1]
wb = openpyxl.load_workbook(f"{D}/ip1910.xlsx", data_only=True)
pop = {r[0]: r[7] for r in openpyxl.load_workbook(f"{D}/insee_2381757.xlsx", data_only=True)["Figure 2"].iter_rows(values_only=True) if isinstance(r[0], int)}
pop.update({1962: 46456, 1968: 49756})  # années éventuellement absentes
ws = wb[" Encadré Figure a"]
hdr = None; part = {}
for r in ws.iter_rows(values_only=True):
    if r[1] == "Belges": hdr = r[1:6]
    elif isinstance(r[0], int) and hdr: part[r[0]] = dict(zip(hdr, r[1:6]))
print("Part (%) × population (milliers) = stock approximatif, arrondi à ±0,05 pt (≈ ±20 k)")
for y in (1931, 1946, 1962):
    p = pop.get(y)
    print(y, p, {k: round(v/100*p) for k, v in part[y].items()} if p else "pop manquante")
print("Italiens 1931 : 2,0 % ->", round(.020*pop[1931]), "k (fourchette", round(.0195*pop[1931]), "-", round(.0205*pop[1931]), ") ; valeur lue (Mourlane) 808 k =", round(808/pop[1931]*100, 2), "%")
print("Italiens 1962 : 1,4 % ->", round(.014*pop[1962] if 1962 in pop else 0), "k ; valeur lue (Mourlane, recensement 1962) 571,684 k =", round(571.684/46456*100, 2), "%  <- ÉCART")
print("Italiens 1946 450 k (Mourlane) ; 1946->1931 :", round(450/808*100-100), "% ; 1946->1968 +26,2 % ->", round(450*1.262), "k")
print("Polonais 1931 : 1,2 % ->", round(.012*pop[1931]), "k ; valeur lue (MNHI) 507,811 k =", round(507.811/pop[1931]*100, 2), "% ; part des étrangers (2714,7 k) =", round(507.811/2714.7*100, 1), "% (MNHI écrit 17,6 %)")
print("Pic de chaque nationalité :", {k: max(part, key=lambda y: part[y][k]) for k in hdr})
