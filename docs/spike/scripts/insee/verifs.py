"""Contrôles croisés sur les fichiers de data/raw/spike/insee/xlsx (lecture seule)."""
import openpyxl, sys
D='data/raw/spike/insee/xlsx/'
def num(x):
    try: return float(str(x).replace('\xa0','').replace(',','.'))
    except: return None
def wb(f): return openpyxl.load_workbook(D+f,data_only=True)
# --- IP2107 : identité immigrés
w=wb('IP2107.xlsx')
ent={str(r[0]).rstrip('e'):num(r[1]) for r in w['Figure 2a'].iter_rows(min_row=4,max_row=22,values_only=True)}
sor={str(r[0]).rstrip('e'):num(r[2]) for r in w['Figure 2a'].iter_rows(min_row=4,max_row=22,values_only=True)}
tc={}
for r in w['Tableau complémentaire 1'].iter_rows(min_row=5,max_row=23,values_only=True):
    tc[str(r[0])]=[num(c) for c in r[1:13]]
print('annee  ent  sor  deces_imm  =ent+sor+solnat  evol_imm(TC1)  ecart  | deces_imm/deces_tot')
bd=wb('demo-pop-composantes.xlsx').active
dec={str(r[0]):num(r[3]) for r in bd.iter_rows(min_row=4,values_only=True) if r[0]}
for y in range(2006,2023):
    t=tc[str(y)]; e=ent[str(y)]; s=sor[str(y)]
    imm_evol=t[1]; solnat_imm=t[4]; calc=e+s+solnat_imm
    d=dec.get(str(y)); print(y,e,s,solnat_imm,round(calc),imm_evol,round(calc-imm_evol),'|',round(-solnat_imm/d*100,1) if d else None,'%')
# --- stocks : delta stock vs evol TC1
st={str(r[0]).split()[0]:num(r[1]) for r in wb('demo-etran-part-pop-etran-immig.xlsx')['Figure 1'].iter_rows(min_row=5,max_row=36,values_only=True) if r[0]}
print('\nDelta stock immigrés (2381757) vs evol TC1 (IP2107)')
for y in range(2007,2024): print(y,round(st[str(y)]-st[str(y-1)],1),tc[str(y-1)][1])
# --- naissances par origine parents
f=wb('demo-naiss-natio-pays-2.xlsx')['Figure 2']
rows=[r for r in f.iter_rows(min_row=3,max_row=16,values_only=True)]
yrs=[c for c in rows[0][1:] if c]
print('\nNaissances (pays de naissance des parents) : années',yrs[0],yrs[-1],len(yrs))
def row(prefix): return [r for r in rows[1:] if r[0] and str(r[0]).strip().startswith(prefix)][0][1:]
a,b,c,t=row('Les deux parents nés en France'),row('Un parent né en France'),row("Les deux parents nés à l'étranger"),row('Ensemble')
for i,y in enumerate(yrs):
    if str(y)[:4] in('1998','2005','2010','2011','2019','2025'):
        print(y,'0 étr',a[i],'1 étr',b[i],'2 étr',c[i],'tot',t[i],'| 2 étr %.1f%% 1 étr %.1f%%'%(100*c[i]/t[i],100*b[i]/t[i]),'| somme ok',a[i]+b[i]+c[i]==t[i])
# --- B2 : 2021 dans 2381755 vs 6793226
p=wb('demo-etran-repart-immig-pays.xlsx')['Figure 1']
hdr=[c for c in next(p.iter_rows(min_row=4,max_row=4,values_only=True))]
i21=hdr.index(2021); print('\n2021 Algérie / Ensemble dans 2381755 :',[ (str(r[0]).strip(),r[i21]) for r in p.iter_rows(min_row=5,max_row=38,values_only=True) if str(r[0]).strip() in('Algérie','Portugal','Ensemble','Afrique')])
# --- descendants
d=wb('demo-etran-origine-desc-immig.xlsx').active
print('descendants 2025 : ensemble',[r[1] for r in d.iter_rows(values_only=True) if r[0]=='Ensemble'],'part un seul parent',[r[3] for r in d.iter_rows(values_only=True) if r[0]=='Ensemble'])
# --- ratio part des décès / part de la population (immigrés), 2006-2022
pop={str(r[0]):num(r[1]) for r in bd.iter_rows(min_row=4,values_only=True) if r[0]}
rat=[]
for y in range(2006,2023):
    sh_d=-tc[str(y)][4]/dec[str(y)]; sh_p=st[str(y)]/pop[str(y)]*1000/1000
    rat.append((y,round(sh_d/ (st[str(y)]/pop[str(y)]),2)))
print('\nratio part décès / part stock (immigrés) :',rat[0],rat[-1],min(r[1] for r in rat),max(r[1] for r in rat))
