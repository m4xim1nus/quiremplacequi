import sys, pdfplumber
with pdfplumber.open(sys.argv[1]) as p:
    print(len(p.pages), "pages")
    for i, pg in enumerate(p.pages, 1):
        print("--- page", i); print(pg.extract_text())
