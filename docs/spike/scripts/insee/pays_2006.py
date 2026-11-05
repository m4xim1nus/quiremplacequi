"""2381755 : lignes pays x années choisies (2006, 2023, 2024, 2025) + en-têtes."""
import sys, openpyxl
ws=openpyxl.load_workbook(sys.argv[1],data_only=True)['Figure 1']
rows=[r for r in ws.iter_rows(min_row=4,max_row=38,values_only=True)]
hdr=[c for c in rows[0] if c is not None]; print(hdr)
ix=[i for i,h in enumerate(hdr) if str(h)[:4] in('2006','2013','2014','2022','2023','2024','2025')]
print([hdr[i] for i in ix])
for r in rows[1:]:
    print(str(r[0]).strip()[:40].ljust(40),[r[i] for i in ix])
