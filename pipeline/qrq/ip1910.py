"""Insee Première 1910 (2022, révisé 2023) : toutes les figures du tableur, en format long.

Diversité des origines et mixité des unions : G1/G2/G3 par âge, origines par âge, généalogies des
G3, origines des parents des G2, origine des conjoints, parts par nationalité 1901-2020. Les en-têtes
sur plusieurs lignes sont concaténés (« Nombre de grands-parents immigrés / Deux ») ; les lignes de
section (« Descendants G3 de moins de 18 ans ») deviennent un `bloc`.
"""

from pathlib import Path

from .lecture import feuille, nombre, texte
from .sources import fichier

FIN = ("Lecture", "Champ", "Source", "Note", "nd :", "1.", "2.", "3.", "Notes")


def lire_ip1910(raw: Path) -> list[dict]:
    import openpyxl

    wb = openpyxl.load_workbook(fichier(raw, "ip1910"), read_only=True)
    noms = wb.sheetnames
    wb.close()
    out = []
    for nom in noms:
        rows = [[texte(c) for c in r] for r in feuille(fichier(raw, "ip1910"), nom)]
        titre = rows[0][0]
        champ = next((r[0] for r in rows if r and r[0].startswith("Champ")), "")
        # Première ligne de données : un libellé et au moins un nombre.
        def est_donnee(r):
            return r and r[0] and any(nombre(c) is not None for c in r[1:])

        i0 = next(i for i, r in enumerate(rows) if i > 0 and est_donnee(r))
        entetes = [r for r in rows[1:i0] if any(c and c != "en %" for c in r[1:])]
        ncol = max(len(r) for r in rows)
        etiquettes = [""] * ncol
        for k, r in enumerate(entetes):
            remplie = ""
            for j in range(1, ncol):
                c = r[j] if j < len(r) else ""
                if c == "en %":
                    c = ""
                if k == 0 and len(entetes) > 1:  # en-tête fusionné : on propage vers la droite
                    remplie = c or remplie
                    c = remplie
                if c:
                    etiquettes[j] = f"{etiquettes[j]} / {c}" if etiquettes[j] else c
        bloc = ""
        for r in rows[i0 - 1 if not est_donnee(rows[i0 - 1]) and rows[i0 - 1][0] else i0 :]:
            if not r or not r[0]:
                continue
            if r[0].startswith(FIN):
                break
            valeurs = [(j, nombre(c)) for j, c in enumerate(r) if j > 0 and nombre(c) is not None]
            if not valeurs:
                bloc = r[0]
                continue
            for j, v in valeurs:
                out.append(
                    {
                        "figure": nom.strip(),
                        "titre": titre,
                        "bloc": bloc,
                        "ligne": r[0],
                        "colonne": etiquettes[j] or str(j),
                        "valeur": round(v, 3),
                        "champ": champ,
                    }
                )
    return out
