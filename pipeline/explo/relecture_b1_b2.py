"""Graphiques bruts de relecture de B1 (série longue) et B2 (vagues), lus dans data/export/.

Pas de mise en forme : servir à repérer à l'œil les sauts, les ruptures de champ, les identités qui
ne bouclent pas et les écarts entre sources. Sorties dans explo/out_figures/ (non versionné), plus un
rapport texte sur la sortie standard. Lancer depuis pipeline/ : uv run python explo/relecture_b1_b2.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import polars as pl

EXPORT = Path(__file__).resolve().parents[2] / "data" / "export"
SORTIE = Path(__file__).resolve().parent / "out_figures"
SORTIE.mkdir(exist_ok=True)

CHAMPS = {"metropole": "#e8eef7", "france_hors_mayotte": "#eef7e8", "france": "#f7f0e8"}
M = 1e6

b1 = pl.read_csv(EXPORT / "b1_stock.csv").sort("annee")
nat = pl.read_csv(EXPORT / "b2_nationalites.csv").sort("annee")
pays = pl.read_csv(EXPORT / "b2_pays.csv").sort("annee")
alertes: list[str] = []


def fonds_champ(ax, df: pl.DataFrame) -> None:
    """Bandes de couleur par champ géographique, ligne verticale aux ruptures de série."""
    lignes = df.select("annee", "champ").rows()
    for i, (a, c) in enumerate(lignes):
        fin = lignes[i + 1][0] if i + 1 < len(lignes) else a + 1
        ax.axvspan(a, fin, color=CHAMPS.get(c, "#eee"), lw=0, zorder=0)
    if "rupture" in df.columns:
        for a in df.filter(pl.col("rupture"))["annee"]:
            ax.axvline(a, color="red", ls="--", lw=1)
            ax.text(a, ax.get_ylim()[1], " rupture", color="red", va="top", fontsize=8)


def sauver(fig, nom: str) -> None:
    fig.tight_layout()
    fig.savefig(SORTIE / nom, dpi=130)
    plt.close(fig)
    print(f"  → {SORTIE / nom}")


# --- B1 ---------------------------------------------------------------------------------------
print("B1")
recens = b1.filter(pl.col("annee") <= 2006)
annuel = b1.filter(pl.col("annee") >= 2006)
prov = b1.filter(pl.col("statut") == "provisoire")
ens = pays.filter(pl.col("pays") == "Ensemble")

# 1. Effectifs : immigrés, étrangers, Français par acquisition ; points de recensement et annuels.
fig, ax = plt.subplots(figsize=(12, 6))
for col, coul in [("immigres", "C0"), ("etrangers", "C1"), ("francais_acquisition", "C2")]:
    ax.plot(b1["annee"], b1[col] / M, color=coul, lw=1, label=col)
    ax.plot(recens["annee"], recens[col] / M, "o", color=coul, ms=5)
    ax.plot(annuel["annee"], annuel[col] / M, ".", color=coul, ms=4)
    ax.plot(prov["annee"], prov[col] / M, "o", mfc="white", color=coul, ms=7)
ax.plot(ens["annee"], ens["immigres"] / M, "x", color="k", ms=8, label="b2_pays « Ensemble »")
fonds_champ(ax, b1)
ax.set(title="B1 — effectifs (millions). ● recensement, · annuel, ○ provisoire ; fond = champ",
       xlabel="année")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
sauver(fig, "b1_1_effectifs.png")

# 2. Parts publiées et recalculées.
b1 = b1.with_columns(
    (100 * pl.col("immigres") / pl.col("population")).alias("part_imm_calc"),
    (100 * pl.col("etrangers") / pl.col("population")).alias("part_etr_calc"),
)
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(b1["annee"], b1["part_immigres"], "o-", ms=4, label="part_immigres (publiée)")
ax.plot(b1["annee"], b1["part_imm_calc"], "+", color="k", label="immigres / population")
ax.plot(b1["annee"], b1["part_etrangers"], "s-", ms=3, label="part_etrangers (publiée)")
ax.plot(b1["annee"], b1["part_etr_calc"], "x", color="k", label="etrangers / population")
fonds_champ(ax, b1)
ax.set(title="B1 — parts dans la population (%)", xlabel="année")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
sauver(fig, "b1_2_parts.png")

# 3. Identités : population = Français de naissance + par acquisition + étrangers ; parts arrondies.
idt = b1.drop_nulls("etrangers").with_columns(
    (pl.col("population") - pl.col("francais_naissance") - pl.col("francais_acquisition")
     - pl.col("etrangers")).alias("residu"),
    (pl.col("part_immigres") - pl.col("part_imm_calc")).alias("ecart_part_imm"),
    (pl.col("part_etrangers") - pl.col("part_etr_calc")).alias("ecart_part_etr"),
)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
a1.bar(idt["annee"], idt["residu"] / 1000, width=0.8)
a1.set(title="population − (Français de naissance + par acquisition + étrangers), milliers")
a2.plot(idt["annee"], idt["ecart_part_imm"], "o", label="part_immigres publiée − calculée")
a2.plot(idt["annee"], idt["ecart_part_etr"], "s", label="part_etrangers publiée − calculée")
a2.axhspan(-0.05, 0.05, color="green", alpha=0.1, label="± arrondi au dixième")
a2.set(title="écarts de parts (points)", xlabel="année")
a2.legend()
for a in (a1, a2):
    a.grid(alpha=0.3)
sauver(fig, "b1_3_identites.png")
for r in idt.iter_rows(named=True):
    if abs(r["residu"]) > 1000:
        alertes.append(f"B1 {r['annee']} : population − somme des nationalités = {r['residu']:+,.0f}")
    for c in ("ecart_part_imm", "ecart_part_etr"):
        if abs(r[c]) > 0.051:
            alertes.append(f"B1 {r['annee']} : {c} = {r[c]:+.2f} point")

# 4. Vitesse : variation annuelle moyenne entre deux points consécutifs.
v = b1.select(
    pl.col("annee").shift(1).alias("de"), pl.col("annee").alias("a"),
    ((pl.col("immigres") - pl.col("immigres").shift(1))
     / (pl.col("annee") - pl.col("annee").shift(1))).alias("par_an"),
    (10 * (pl.col("part_imm_calc") - pl.col("part_imm_calc").shift(1))
     / (pl.col("annee") - pl.col("annee").shift(1))).alias("points_decennie"),
    pl.col("champ"), pl.col("champ").shift(1).alias("champ_avant"),
).drop_nulls("de")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
for a, col, tit in [(a1, "par_an", "immigrés par an (milliers)"),
                    (a2, "points_decennie", "points de part par décennie")]:
    coul = ["red" if c != p else "C0" for c, p in zip(v["champ"], v["champ_avant"])]
    a.bar([(d + f) / 2 for d, f in zip(v["de"], v["a"])],
          v[col] / (1000 if col == "par_an" else 1),
          width=[f - d - 0.3 for d, f in zip(v["de"], v["a"])], color=coul)
    a.axhline(0, color="k", lw=0.5)
    a.set(title=f"B1 — variation annuelle moyenne : {tit} (rouge = changement de champ)")
    a.grid(alpha=0.3)
a2.set_xlabel("intervalle entre deux points")
sauver(fig, "b1_4_vitesse.png")

# Écart entre b1 et b2_pays « Ensemble » aux années communes.
for r in ens.join(b1, on="annee").iter_rows(named=True):
    e = r["immigres"] - r["immigres_right"]
    if abs(e) > 1000:
        alertes.append(f"B1/B2 {r['annee']} : b2_pays Ensemble − b1 = {e:+,} (sources ou millésimes différents ?)")

# --- B2 ---------------------------------------------------------------------------------------
print("B2")

# 5. Nationalités : part dans la population, petits multiples à échelle commune.
noms = nat.select("nationalite", "groupe").unique(maintain_order=True).rows()
fig, axes = plt.subplots(3, 5, figsize=(16, 9), sharex=True, sharey=True)
for ax, (n, g) in zip(axes.flat, noms):
    d = nat.filter(pl.col("nationalite") == n)
    ax.plot(d["annee"], d["part_pct"], "o-", ms=3, color={"europe": "C0", "afrique": "C1"}.get(g, "C2"))
    ax.set_title(n, fontsize=9)
    ax.grid(alpha=0.3)
for ax in list(axes.flat)[len(noms):]:
    ax.axis("off")
fig.suptitle("B2 — étrangers par nationalité, % de la population (échelle commune)")
sauver(fig, "b2_1_nationalites.png")

# Somme des nationalités détaillées par année (pas un total : les « autres » européens manquent).
for a, s in nat.group_by("annee").agg(pl.col("part_pct").sum()).sort("annee").rows():
    ref = b1.filter(pl.col("annee") == a)["part_etrangers"]
    if len(ref) and ref[0] is not None and s > ref[0] + 0.05:
        alertes.append(f"B2 {a} : somme des nationalités {s:.1f} % > part des étrangers B1 {ref[0]} %")

# 6. Pays de naissance détaillés, petits multiples en effectifs.
detail = ["Espagne, Italie", "Portugal", "Algérie", "Maroc, Tunisie", "Afrique sahélienne",
          "Afrique guinéenne ou centrale", "Autres pays d'Afrique", "Turquie", "Chine",
          "Asie du Sud-Est", "Autres pays d'Asie", "Autres pays d'Europe", "Pays de l’UE27",
          "Amérique, Océanie", "Ensemble"]
fig, axes = plt.subplots(3, 5, figsize=(16, 9), sharex=True)
for ax, p in zip(axes.flat, detail):
    d = pays.filter(pl.col("pays") == p)
    ax.plot(d["annee"], d["immigres"] / 1000, "o-", ms=3)
    fonds_champ(ax, d)
    ax.set_title(p, fontsize=9)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)
fig.suptitle("B2 — immigrés par pays de naissance (milliers, échelles libres) ; fond = champ")
sauver(fig, "b2_2_pays.png")

# 7. Emboîtements : chaque agrégat contre la somme de ses parties.
EMBOITEMENTS = {
    "Maghreb": ["Algérie", "Maroc, Tunisie"],
    "Afrique": ["Maghreb", "Afrique sahélienne", "Afrique guinéenne ou centrale", "Autres pays d'Afrique"],
    "Asie": ["Turquie", "Chine", "Asie du Sud-Est", "Autres pays d'Asie"],
    "Europe du Sud": ["Espagne, Italie", "Portugal"],
    "Europe": ["Europe du Sud", "Autres pays d'Europe"],
    "Ensemble": ["Afrique", "Asie", "Europe", "Amérique, Océanie"],
}
large = pays.pivot(on="pays", index="annee", values="immigres").sort("annee")
fig, ax = plt.subplots(figsize=(12, 5))
for i, (tot, parts) in enumerate(EMBOITEMENTS.items()):
    ecart = large[tot] - large.select(pl.sum_horizontal(parts)).to_series()
    ax.plot(large["annee"] + (i - 2.5) * 0.4, ecart / 1000, "o", label=f"{tot} − Σ parties")
    for a, e, *vals in zip(large["annee"], ecart, *[large[p] for p in parts]):
        manque = [p for p, x in zip(parts, vals) if x is None]
        if manque and abs(e) > 2000:
            alertes.append(f"B2 {a} : {tot} − Σ = {e:+,} ; parties non publiées : {', '.join(manque)}")
        elif not manque and abs(e) > 2000:
            alertes.append(f"B2 {a} : {tot} − Σ parties = {e:+,}")
ax.axhline(0, color="k", lw=0.5)
ax.set(title="B2 — agrégat − somme de ses parties (milliers ; 0 attendu à l'arrondi près)",
       xlabel="année")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
sauver(fig, "b2_3_emboitements.png")

print(f"\n{len(alertes)} alerte(s)")
for a in alertes:
    print(" -", a)
