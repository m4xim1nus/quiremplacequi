import sys, pymupdf
src, outdir, pages = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
d = pymupdf.open(src)
for n in pages:
    d[n-1].get_pixmap(dpi=60).save(f"{outdir}/p{n:02d}.png")
