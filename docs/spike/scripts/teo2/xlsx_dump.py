import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
maxr = int(sys.argv[2]) if len(sys.argv) > 2 else 12
for ws in wb.worksheets:
    print("##", ws.title, ws.max_row, "x", ws.max_column)
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i >= maxr: break
        r = [str(c)[:60] for c in row if c is not None]
        if r: print("  ", r)
