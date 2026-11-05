"""2381757 : séries complètes immigrés/étrangers + notes ; contrôle de cohérence."""
import sys, openpyxl
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
for ws in wb:
    print('\n###',ws.title)
    for r in ws.iter_rows(values_only=True):
        v=[str(c).replace('\n',' ') for c in r if c is not None]
        if v: print(v)
