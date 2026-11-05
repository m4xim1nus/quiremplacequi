"""IP 2107 : séries complètes des flux (Fig. 1, 2a, 2b, Tableau compl. 1) + notes."""
import sys, openpyxl
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
for name in ['Figure 1','Figure 2a','Figure 2b','Tableau complémentaire 1']:
    ws=wb[name]; print('\n###',name)
    for r in ws.iter_rows(min_col=1,max_col=14,values_only=True):
        if any(c is not None for c in r):
            print([c if c is None else str(c).replace('\n',' ') for c in r if c is not None])
