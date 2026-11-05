"""Choix de la forme des départs d'immigrés par âge (referentiels/cohortes.yaml) : grille de poids,
taux recalé sur les sorties Insee, erreur = écart quadratique à la part des G1 par âge en 2019-2020
(IP 1910). Lancer depuis pipeline/ : uv run python explo/calage_departs.py"""
from pathlib import Path
import yaml, numpy as np, itertools
from qrq import cohortes as C, stock, bilan, naissances, flux
R=Path('../data/raw')
p=yaml.safe_load(open('referentiels/cohortes.yaml'))
e=C.preparer(R, stock.lire_stock(R), bilan.lire_bilan(R), naissances.lire_naissances_parents(R), p)
cib=[c for c in C.lire_cibles_ip1910(R) if c['classe'] not in ('0-17','18-59','0-59','60 ou plus','Ensemble')]
fl={f['annee']:f for f in flux.lire_flux(R)}
sorties={t:fl[t]['sorties_imm'] for t in fl if fl[t]['sorties_imm'] is not None}
coh=C.parts_cohortes(C.lire_cibles_ip1910(R))
pop=C._vecteur(e.ages,2020)
res=[]
for wy, wr, wv in itertools.product([1,2,3,4],[1,1.5,2,3],[0.5,1]):
    pp={**p,'departs':{**p['departs'],'forme':[{'de':0,'a':14,'poids':0.5},{'de':15,'a':17,'poids':1},{'de':18,'a':29,'poids':wy},{'de':30,'a':54,'poids':1},{'de':55,'a':69,'poids':wr},{'de':70,'a':105,'poids':wv}]}}
    per=range(2006,2022)
    def ec(tx):
        pp['departs']['taux']=tx
        sim={a['annee']:a for a in C.simuler(e,pp,coh,seul_g1=True)['annees']}
        return np.mean([sim[t]['departs_G1'] for t in per])-np.mean([sorties[t] for t in per])
    tx=C._bissection(ec,0,0.2)
    pp['departs']['taux']=tx
    sim={a['annee']:a for a in C.simuler(e,pp,coh,seul_g1=True)['annees']}
    err=sum((C.parts_par_classe(sim[2020]['etat'],pop,c['classe'])['G1']-c['G1'])**2 for c in cib)
    d=np.mean([sim[t]['deces_G1'] for t in per]); di=np.mean([fl[t]['deces_imm'] for t in per])
    res.append((err,wy,wr,wv,round(tx,4),round(d/di,3)))
for r in sorted(res)[:6]: print(r)
