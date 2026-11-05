"""Bilan démographique (POP1, 8999013) : onglets, bornes, années clés, + décès 1946-."""
import sys, openpyxl
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
for ws in wb:
    print('###',ws.title,ws.dimensions)
    rows=[r[:12] for r in ws.iter_rows(values_only=True)]
    for r in rows[:4]: 
        if any(r): print([str(c).replace('\n',' ')[:60] for c in r if c is not None])
    for r in rows:
        if r[0] is not None and str(r[0]).strip() in ('1946','1950','1962','1968','1975','1982','1990','1999','2006','2022','2025','2026'):
            print([str(c).strip() if c is not None else '' for c in r])
    for r in rows[-12:]:
        if r[0] and not str(r[0]).strip().isdigit(): print('  note:',str(r[0])[:230])
