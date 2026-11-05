"""Affiche les onglets d'un xlsx : dimensions + premières/dernières lignes non vides.
Usage : python -I dump.py fichier.xlsx [max_lignes] [max_cols]"""
import sys, openpyxl
f=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 12; mc=int(sys.argv[3]) if len(sys.argv)>3 else 10
wb=openpyxl.load_workbook(f,data_only=True)
for ws in wb:
    print(f"\n### {ws.title} dims={ws.dimensions}")
    rows=[(i+1,[c for c in r[:mc]]) for i,r in enumerate(ws.iter_rows(values_only=True)) if any(c is not None for c in r)]
    sel=rows[:n]+([("...",[])]+rows[-4:] if len(rows)>n+4 else rows[n:])
    for i,r in sel:
        print(i,[ (round(c,4) if isinstance(c,float) else (str(c)[:70] if c is not None else None)) for c in r])
