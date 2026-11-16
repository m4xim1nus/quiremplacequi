"""Image de partage (Open Graph, 1200 × 630) : le titre et l'échelle de l'accueil, chiffres lus dans
data/export/b1_stock.csv (même règle que l'accueil : premier point affiché, sommets d'avant 1946 et de
1946-1989, dernier point). Écrit site/static/partage.png, versionné (le build de Cloudflare ne
dessine rien). Relancer après une mise à jour des données :

    uv run --with pillow --with fonttools --with brotli python site/scripts/partage.py
"""

import csv
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parents[2]
POLICES = RACINE / "site/static/fonts"
DEBUT = 1921  # première année de la piscine et de l'accueil

PAPIER, PLAQUE, ENCRE, ARDOISE, REGLURE = "#f6f7f5", "#ffffff", "#15212b", "#4c5a65", "#ccd4d8"
REPERE, EAU = "#b07d0c", "#002c9c"


def police(nom: str, taille: int, poids: int | None = None) -> ImageFont.FreeTypeFont:
    """Police woff2 du site, décompressée en mémoire ; `poids` pour une police variable."""
    f = TTFont(POLICES / nom)
    f.flavor = None
    tampon = io.BytesIO()
    f.save(tampon)
    tampon.seek(0)
    p = ImageFont.truetype(tampon, taille)
    if poids is not None:
        p.set_variation_by_axes([poids])
    return p


def serie() -> list[tuple[int, float]]:
    with open(RACINE / "data/export/b1_stock.csv", encoding="utf-8") as f:
        lignes = [(int(r["annee"]), float(r["part_immigres"])) for r in csv.DictReader(f) if r["part_immigres"]]
    return sorted(x for x in lignes if x[0] >= DEBUT)


def main() -> None:
    s = serie()
    sommet = lambda de, a: max((x for x in s if de <= x[0] < a), key=lambda x: x[1])
    reperes = [s[0], sommet(DEBUT, 1946), sommet(1946, 1990), s[-1]]
    niveau = s[-1][1]

    im = Image.new("RGB", (1200, 630), PAPIER)
    d = ImageDraw.Draw(im)
    titre = police("barlow-semi-condensed-latin-700-normal.woff2", 118)
    titre_p = police("barlow-semi-condensed-latin-600-normal.woff2", 26)
    plaque_g = police("barlow-semi-condensed-latin-700-normal.woff2", 24)
    plaque_v = police("barlow-semi-condensed-latin-500-normal.woff2", 22)
    texte = police("atkinson-hyperlegible-next-latin-wght-normal.woff2", 34, 400)
    petit = police("atkinson-hyperlegible-next-latin-wght-normal.woff2", 24, 400)

    # Texte à gauche.
    d.text((72, 100), "Qui remplace", font=titre, fill=ENCRE)
    d.text((72, 212), "qui ?", font=titre, fill=ENCRE)
    d.rectangle((72, 396, 72 + 70, 402), fill=REPERE)
    d.multiline_text(
        (72, 424),
        "La démographie des migrations en France,\nmesurée avec la statistique publique.",
        font=texte, fill=ARDOISE, spacing=10,
    )
    d.text((72, 548), "quiremplacequi.technoperchoir.fr", font=petit, fill=ARDOISE)

    # Échelle limnimétrique à droite : 0 à MAX %, graduations en « E ».
    mx = 2 * int((niveau + 1.5) // 2 + 1)
    x, w, h0, h1 = 820, 92, 590, 40
    y = lambda p: h0 - (p / mx) * (h0 - h1)
    u = (h0 - h1) / mx
    d.rectangle((x, h1, x + w, h0), fill=PLAQUE, outline=REGLURE, width=2)
    eau = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(eau).rectangle((x, y(niveau), x + w, h0), fill=(0, 44, 156, 40))
    im.paste(eau, (0, 0), eau)
    d = ImageDraw.Draw(im)
    for n in range(mx):
        gauche = n % 2 == 0
        xs = x + 6 if gauche else x + w / 2
        lg = w / 2 - 6
        for k in range(3):
            yy = y(n + 0.1 * (2 * k + 1))
            d.rectangle((xs, yy - u * 0.1, xs + lg, yy), fill=ENCRE)
        xb = xs if gauche else xs + lg - u * 0.1
        d.rectangle((xb, y(n + 0.5), xb + u * 0.1, y(n)), fill=ENCRE)
        if n % 2 == 0:
            lib = "0" if n == 0 else f"{n} %"
            d.text((x - 14, y(n)), lib, font=titre_p, fill=ENCRE, anchor="rm")
    d.text((x - 14, y(mx)), f"{mx} %", font=titre_p, fill=ENCRE, anchor="rm")
    d.line((x - 8, y(niveau), x + w + 8, y(niveau)), fill=EAU, width=5)

    # Plaques des repères, de bas en haut, au moins 56 px d'écart.
    precedent = 10_000
    for an, part in sorted(reperes, key=lambda r: r[1]):
        yn = y(part)
        yp = min(yn, precedent - 56)
        precedent = yp
        couleur = EAU if an == s[-1][0] else REPERE
        d.line([(x + w, yn), (x + w + 14, yn), (x + w + 14, yp), (x + w + 22, yp)], fill=REPERE, width=3)
        d.rectangle((x + w + 22, yp - 24, x + w + 22 + 116, yp + 26), fill=PLAQUE, outline=couleur, width=3)
        d.text((x + w + 34, yp - 2), str(an), font=plaque_g, fill=ENCRE, anchor="ls")
        d.text((x + w + 34, yp + 20), f"{part:.1f} %".replace(".", ","), font=plaque_v, fill=ARDOISE, anchor="ls")

    sortie = RACINE / "site/static/partage.png"
    im.save(sortie, optimize=True)
    print(f"{sortie.relative_to(RACINE)} : {sortie.stat().st_size // 1024} Ko ; repères {reperes}")


if __name__ == "__main__":
    main()
