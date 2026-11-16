"""Répartition annuelle du flux net d'immigrés avant 2006 (BACKLOG : 1974 invisible).
Entre deux recensements, le flux net total des immigrés est fixé par les stocks. Trois façons de le
répartir par année : celle de l'export courant (colonnes « lin » : linéaire jusqu'au 2026-11-16,
« solde_bilan » depuis, identique à « add »), additive (solde des non-immigrés constant, toute la
variation annuelle du solde migratoire du bilan va aux immigrés), proportionnelle (flux net des
immigrés ∝ solde migratoire du bilan). Lancer depuis pipeline/ : uv run python explo/flux_avant_2006.py
"""
import json
from pathlib import Path

P = json.loads(Path("../data/export/piscine.json").read_text())
A = {x["annee"]: x for x in P["annees"]}
RECS = [1968, 1975, 1982, 1990, 1999, 2006]

print(f"{'an':5} {'SM':>8} | {'imm lin':>8} {'ni lin':>8} | {'imm add':>8} {'ni add':>8} | {'imm prop':>8} {'ni prop':>8}")
for r0, r1 in zip(RECS, RECS[1:]):
    ans = range(r0, r1)
    sm = {a: A[a]["net_imm"] + A[a]["net_ni"] for a in ans}
    tot = sum(A[a]["net_imm"] for a in ans)
    c = (tot - sum(sm.values())) / len(ans)
    for a in ans:
        add = sm[a] + c
        prop = tot * sm[a] / sum(sm.values())
        print(f"{a:5} {sm[a]:8.0f} | {A[a]['net_imm']:8.0f} {A[a]['net_ni']:8.0f} | {add:8.0f} {sm[a]-add:8.0f} | {prop:8.0f} {sm[a]-prop:8.0f}")
    print("-" * 80)
