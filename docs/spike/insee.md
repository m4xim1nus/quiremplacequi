# Spike sources : données Insee contemporaines (1946/1968 → 2025)

Vérifié les 2026-11-04 et 2026-11-05 sur insee.fr (pages, xlsx, PDF) et sur l'API BDM. Toute valeur
ci-dessous est lue par script (`docs/spike/scripts/insee/` : `dump.py`, `ip2107.py`, `stock.py`,
`pays_2006.py`, `bilan.py`, `verifs.py`) sur les fichiers de `data/raw/spike/insee/` (non versionnés ;
sortie des contrôles croisés : `data/raw/spike/insee/verifs_sortie.txt`). ✅ vérifié, 🔎 non trouvé.

**Licence** : Licence Ouverte 2.0 (Etalab) par défaut sur insee.fr, mention « Source : Insee » et date de
mise à jour (`https://www.insee.fr/fr/information/2008466`) ✅. Pas de mention contraire sur les pages lues.
Page d'un jeu : `https://www.insee.fr/fr/statistiques/<id>` ; fichier : `/fr/statistiques/fichier/<id>/<nom>`.

## 1. Tableau des jeux

| Jeu (page → fichier) | Période, granularité | Champ | Statut / mise en ligne | Verdict |
|---|---|---|---|---|
| **Flux IP 2107** `8998082` → `IP2107.xlsx` (+ `IP2107.pdf`) | annuel 2006-2022 : entrées, sorties, décès (via solde naturel), croissance, pour immigrés / non-immigrés / ensemble ; entrées seules 2023-2024 ; fig. 3, 4, TC2, TC3 : profil des entrants 2024 | hors Mayotte jusqu'en 2013, France ensuite | 2020 « e » (estimé) ; 2023-24 sorties `nd` ; paru 04/06/2026 | **GO** (2006+) |
| **Stock** `2381757` → `demo-etran-part-pop-etran-immig.xlsx` | 1921, 26, 31, 36, 46, 54, 62, 68, 75, 82, 90, 99, puis annuel 2006-2025 ; immigrés, Français de naissance, par acquisition, étrangers | métropole 1921-82 ; hors Mayotte 1990-2013 ; France dès 2014 | 2024-25 provisoires, **rupture 2024** ; paru 04/06/2026 | **GO** |
| Décomposition lieu de naissance × nationalité `2865118` → `demo-etran-decompo-pop.xlsx` | annuel 2006-2025 : nés en France (F/E), nés à l'étranger **Français non immigrés**, immigrés naturalisés, immigrés étrangers | hors Mayotte jusqu'en 2013, puis avec | idem, rupture 2024 | **GO** (distingue immigrés / Français nés à l'étranger) |
| **Pays** `2381755` → `demo-etran-repart-immig-pays.xlsx` | annuel 2006-2025, effectifs + % | idem | idem | **GO** (granularité faible) |
| **Pays long** `6793226` → `IMMFRA23-F2.xlsx` | 8 coupes seulement : 1968, 75, 82, 90, 99, 2006, 2010, 2021 (+ série de totaux depuis 1911) | métropole 1968-90, hors Mayotte 1999-2013, France ensuite | paru 30/03/2023, erratum 24/05/2024 ; 2020-21 provisoires | **GO partiel** |
| **Naissances / parents** `2381382` → `demo-naiss-natio-pays-2.xlsx` | annuel 1998-2025, 2 onglets (nationalité, pays de naissance) | hors Mayotte jusqu'en 2013, France ensuite | état civil, paru 06/07/2026 | **GO** |
| **Descendants origine** `4186761` → `demo-etran-origine-desc-immig.xlsx` | **2025 seulement**, effectifs, % un seul parent immigré | hors Mayotte, **logement ordinaire**, enquête Emploi | paru 22/06/2026 | **GO** (un millésime) |
| **Descendants âge** `4187125` → `demo-etran-struct-age-desc-origine.xlsx` | 2025, 4 classes d'âge × origine | idem | idem | **GO** (classes larges) |
| **Âge des immigrés** `2381759` → `demo-etran-pop-sexe-age.xlsx` | 1990, 99, 2007, 12, 17, 21-25 ; % en 4 classes (<15, 15-24, 25-54, ≥55), % hommes | hors Mayotte puis France | rupture 2024 | **partiel** |
| IP 1910 `6468640` → `ip1910.xlsx` | G1/G2/G3 par classe d'âge de 5 ans (enquête Emploi 2019-20 + TeO2 pour les G3 de 18-59) | métropole, logement ordinaire | paru 05/07/2022 | **GO** pour F2 |
| **Bilan démographique** `8999013` → `1_Pop_annu_compo_evol.xlsx` | onglet `FM` : naissances et décès 1901-2026, population au 1er janvier et solde migratoire depuis 1946 ; `FR` dès 1957 ; `FM-histo` 1806-1900 | FM = métropole frontières actuelles ; FR = hors Mayotte puis France | 2023-25 provisoires | **GO** |
| Composantes `2381468` → `demo-pop-composantes.xlsx` | 1982-2026 : population, naissances, décès, soldes, ajustement | hors Mayotte jusqu'en 2013, puis France | idem | **GO** (France, mais 1982+) |
| Naissances `8999017` (`1_Naissances_tnat.xlsx`) ; décès `8999019` (`1_Deces_tmort.xlsx`, `4_Survivants`, `3_Quotients_mortalite`) ; pop. par âge `8999013` (`3_Pop1janv_age.xlsx`) | séries longues (naissances dès 1901) | FM et FR | « La situation démographique en 2025 et en séries longues » | **GO** (tables de mortalité pour modéliser les décès d'immigrés) |
| **Projections IP 2108** `9004289` → `ip2108.xlsx` | 2026-2070 ; 9 scénarios sur la population totale (fig. 3) | France | paru 08/06/2026 | **GO** (total uniquement) |

## 2. La piscine 1968 → 2025 : les quatre vannes

| Vanne | Population totale | Immigrés | Non-immigrés |
|---|---|---|---|
| Naissances | ✅ annuel 1901-2025 (`FM`) / 1982-2025 France | ✅ nulles par définition | ✅ 2006-2022 (IP 2107, onglet Fig. 1 pour 2022 ; TC1 par différence) ; = total des naissances |
| Décès | ✅ annuel | ✅ **2006-2022 seulement**, par le solde naturel (TC1, `Tableau complémentaire 1`, colonnes « Solde naturel – Immigrés ») | ✅ 2006-2022 |
| Entrées | 🔎 pas de série d'entrées totales avant 2006 (seulement le solde migratoire) | ✅ 2006-2024 (Fig. 2a) | ✅ 2006-2024 (Fig. 2b) |
| Sorties | 🔎 idem | ✅ 2006-2022 (Fig. 2a ; 2023-24 `nd`) | ✅ 2006-2022 (Fig. 2b) |

Verdict **piscine 1968-2025 : partiel**. Les quatre vannes séparées existent pour 2006-2022 (17 années). Pour 2023-2024 il y a les
entrées seules. Pour 1968-2005 il n'y a aucune ventilation par statut migratoire, seulement le total (naissances, décès, solde migratoire résiduel).

- ✅ **Décès d'immigrés non observés** : « les statistiques de l'état civil ne permettent pas de savoir si une personne décédée est immigrée »
  (IP 2107 PDF, encadré Méthodes). Ils sont modélisés par l'Insee à partir de la mortalité. Ils représentent 9,1 % des décès totaux en 2006,
  10,5 % en 2022 (script `verifs.py`) ; rapport part des décès / part du stock immigrés : 0,98 à 1,12 sur 2006-2022 (1,12 en 2006, 1,02 en 2022).
- ✅ **Contrôle de l'identité** : entrées + sorties + solde naturel des immigrés redonnent l'évolution de TC1 à ±1 000 près sur 2006-2022
  (exemple 2022 : 375 − 26 − 71 = 278 contre 277, arrondi). Le stock de la série `2381757` s'en écarte de 5 à 10 milliers certaines années
  (réajustements 2019-2023) et de **+60 milliers en 2014 : entrée de Mayotte dans le champ** (192 contre 132).
- ✅ Les sorties sont un résidu : « estimées par différence entre le solde migratoire et les entrées » (même encadré). Série des sorties
  d'immigrés (milliers) : 71, 91, 95, 106, 109, 96, 104, 92, 65, 94, 66, 93, 83, 125, 94 (2020e), 123, **26** (2022).
- ✅ Population totale 2022, Fig. 1 : naissances 726 (tous non-immigrés), décès 675 (71 d'immigrés), entrées 490 (375 + 115), sorties 219 (26 + 193).
- **Reconstruction 1968-2005 (à décider avec Max)** : stocks de recensement (1968 : 3 238 ; 1975 : 3 887 ; 1982 : 4 037 ; 1990 : 4 222 ;
  1999 : 4 374 ; 2006 : 5 136 milliers) ; flux net des immigrés = Δstock + décès d'immigrés, ces derniers estimés au rapport 1,0-1,15
  × part du stock dans la population × décès totaux (hypothèse à calibrer sur 2006-2022 et à afficher). Entrées et sorties ne sont **pas
  séparables** avant 2006 (seul le solde net), et le solde migratoire total des bilans est lui-même un résidu (U1). Écart de champ à gérer :
  métropole jusqu'en 1982, avec rapatriements de 1962 dans le solde (860 200 en 1962, onglet `FM`).
- **Structure par âge des immigrés** : seulement 4 classes d'âge en % (`2381759`), plus la table IMG1 du recensement (7 257 155 immigrés en 2023
  d'après un extrait de résultat de recherche, par sexe et 4 classes ; 🔎 table non téléchargée ni lue) ; classes de 5 ans en part de la population, 2019-20, via IP 1910 (G1 : 0,8 % des 0-4 ans, 14,4 % des 35-39 ans, 7,9 % des 80 ans ou plus).
  Pyramide fine des immigrés : 🔎 non publiée en tableur ; piste = fichiers détail du recensement (non testés). Pour la structure totale :
  `3_Pop1janv_age.xlsx` (âge simple).
- **Âge à l'arrivée** (nouveaux entrants 2024, Fig. 3) : médian 26 ans (immigrés), quartiles 19 / 36 ; Afrique hors Maghreb 23 ans.

## 3. Naissances selon l'origine des parents (`2381382`)

✅ Onglet 2 (« pays de naissance des parents »), 1998-2025, 28 années, la somme des trois blocs = Ensemble toutes années (testé).
Part des naissances : deux parents nés à l'étranger 9,4 % (1998), 12,2 % (2011), 17,2 % (2019), **19,4 % (2025 : 124 676 sur 643 905)** ;
un seul parent né à l'étranger 13,8 % (1998), 15,1 % (2025 : 97 358) ; aucun 421 871 (2025).

- **Verdict GO**, avec trois réserves. (1) « Né à l'étranger » ≠ immigré : inclut les Français nés à l'étranger ; les parents nés en COM sont
  classés « nés en France ». (2) **Rupture 2010→2011** (changement de méthode, mentionnée en note) : un parent étranger 134 891 → 119 114,
  deux parents 91 658 → 100 203. (3) Depuis 2023 le « second parent » peut être la mère n'ayant pas accouché (99,5 % de pères en 2025).
- Ventilation UE27 / hors UE27 (UE à 27 actuelle, pas celle du moment) ; pas de pays, pas de détail Maghreb. Nationalité des parents : onglet 1.
- Départemental 2025 : `9000191` (xlsx `n*d`, zip) ; non exploité. Naissances totales identiques au bilan (725 997 en 2022 ✅).

## 4. B1 et B2

**B1 : GO.** `2381757`, onglet « Figure 1 » (immigrés) et « Figure 2 » (étrangers, Français par acquisition, Français de naissance).
Valeurs 2025 (p) : immigrés 7 970 milliers, 11,6 % ; étrangers 6 297,4 (9,1 %) ; Français par acquisition 3 335,7 ; population 68 852. 2024 (p, rupture) : 7 749 (11,3 %).
Non annuel avant 2006 : 1921, 26, 31, 36, 46, 54, 62, 68, 75, 82, 90, 99 (et 1911 : 1 110 milliers, 2,8 %, dans `6793226`). Avant 1968 le chiffre est celui
des immigrés **recensés en métropole** (même note de définition, « nés de nationalité étrangère à l'étranger ») ; la série SGF par nationalité 1851-2008 est 🔎
(trouvé : `…/fichier/1374019/IMMFRA12_g_Flot1_pop.pdf`, PDF, non extrait).
- **Rupture 2024** ✅ (note `…/fichier/2383177/Note_methodo_rupture_serie_immigration.pdf`, 04/06/2026) : cause = nouveau protocole « Recens'Smart »
  (réponse internet sur smartphone, meilleure identification du statut d'immigré). Hausse apparente 2023→2024 : +440 000 immigrés, +425 000 étrangers.
  Effet structure estimé : +242 000 immigrés / −242 000 non-immigrés (effet total de la collecte 271 000 sur la population). **Hausse corrigée : +198 000
  immigrés (+0,3 pt) et +260 000 étrangers.** Les niveaux 2024-2025 ne sont pas corrigés dans le tableur : l'Insee déconseille de les comparer aux années avant 2024.
  Dans la note, une légende de figure donne « 11,0 % » en 2025 contre 11,6 % dans le tableur (coquille probable).
- Autres limites : champ (métropole → hors Mayotte → France entière dès 2014), données 2019-2023 « réajustées » (absence d'EAR 2021).

**B2 : partiel.** Granularité :
- `2381755` (2006-2025, annuel) : Afrique (Maghreb : Algérie ; Maroc + Tunisie réunis ; Afrique sahélienne ; guinéenne ou centrale ; Comores + Madagascar ; autres),
  Asie (Turquie, Moyen-Orient, Asie du Sud-Est, Chine, Asie du Sud, autres), Europe (Portugal ; **Espagne + Italie réunies** ; autres UE15 ; autres UE27 ; Royaume-Uni ; autres), Amériques/Océanie.
  Pas de Pologne, Belgique ni Italie seule. 2025 : Algérie 1 008,1 ; Maroc + Tunisie 1 325,3 ; Portugal 572,5 ; Espagne + Italie 512,2 ; Turquie 275,4 ; Royaume-Uni 147,5 ; Afrique 3 923,2 (49,2 %).
- `6793226` : mêmes regroupements mais 8 dates (Afrique sahélienne / guinéenne `nd` avant 2006) ; 1968 : Espagne + Italie 1 456, Portugal 282, Algérie 378 ; 1975 : Portugal 655.
- ✅ **Rupture de champ 2013→2014** visible : Comores + Madagascar passe de 90,0 à 153,1 milliers (Mayotte). 2021 diffère entre fichiers (Algérie 887 contre 875,9 ; ensemble 6 964 contre 6 932,4) : provisoire contre réajusté.
- Vagues « Belgique, Pologne » du cadrage : impossibles avec ces fichiers (🔎 série IMMFRA12 par nationalité).

## 5. F2 : descendants et définitions

**GO** pour le curseur sur 2025 et pour une photo par âge ; **pas de série temporelle** de descendants.
- ✅ 2025 (enquête Emploi, hors Mayotte, logement ordinaire) : 8 030 milliers de descendants d'immigrés dont 55 % n'ont qu'un parent immigré (onglet « Données », ligne Ensemble) ; origine : Afrique 3 879 (48,3 %), Europe 2 938, Asie 840 ; par âge (Fig. 1 de `4187125`) : moins de 15 ans 2 428, 15-24 ans 1 456, 25-54 ans 2 559, 55 ans ou plus 1 587. Europe du Sud : 62 % des descendants Espagne/Italie ont 55 ans ou plus.
  Pour les 75 ans ou plus, ce sont des estimations (note). Origine du père si deux parents immigrés.
- ✅ **G3 Insee** : seulement IP 1910 (enquête Emploi 2019-2020, métropole ; TeO2 pour les 18-59 ans), G3 nd après 59 ans. Parts, 0-59 ans : G1 9,1 %, G2 13,4 % (deux parents 7,1 + un parent 6,3), G3 10,2 % (quatre grands-parents immigrés 0,6 + mixtes 9,6), ni G1-G2-G3 67,3 %. À 18-59 ans : G1 11,9 / G2 10,6 / G3 9,4 / reste 68,1. G3 : 91 % des 18-59 ans ont ≥ 1 grand-parent immigré né en Europe (58 % ES/IT/PT) ; G2 de 60 ans ou plus : 91 % d'origine européenne ; 5 % des G3 de 18-59 ans ont 4 grands-parents immigrés (20 % pour le Maghreb) (texte de la page).
- `2865118` isole les Français nés à l'étranger (non immigrés) des immigrés : indispensable pour ne pas confondre « né à l'étranger » (naissances par parents) et « immigré ».
- Champs différents pour les mêmes mots : stock G1 (recensement, population totale, France) contre descendants (enquête Emploi, logement ordinaire, hors Mayotte) : à badger (U6).

## 6. Bilans et séries longues, API

- ✅ **API BDM sans clé** : `https://api.insee.fr/series/BDM/V1/data/SERIES_BDM/<idbank>` répond 200 en SDMX-ML sans authentification (idem miroir
  `https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/<idbank>`) ; liste des 229 dataflows : `…/dataflow/FR1/all` ; `?startPeriod=` et `?lastNObservations=1` fonctionnent.
  Exemple : `000436391` = naissances mensuelles métropole, 1946-01 → 2026-09, `LAST_UPDATE` 2026-10-29, mensuel provisoire. Dataflows utiles :
  `NAISSANCES-FECONDITE`, `DECES-MORTALITE`, `POPULATION-STRUCTURE` (plusieurs séries « arrêtées »). **Aucun dataflow immigrés ni flux** (fichiers xlsx obligatoires).
  Un appel sur le dataflow entier `DEMOGRAPHIE-ESTIMATIONS-POPULATION` renvoie une erreur 500 (nom inexistant). Conclusion : `download` possible pour naissances/décès ; xlsx pour le reste.
- ✅ Bilan, onglet `FM`, exemples : 1946 : population 40 125 230, naissances 843 904, décès 545 880, solde migratoire 25 000 ; 1968 : 49 723 072, 835 796, 553 441, 102 308 ; 1962 : solde migratoire 860 200 ; 2022 : 65 846 255, 686 564, 658 434, 269 485.
  Population France : `demo-pop-composantes.xlsx` 1982 : 55 572 624 ; 2025 : 68 851 996 ; 2026 : 69 081 996.
- ✅ 2023, 2024, 2025 : **solde migratoire 176 000 par convention** (moyenne 2020-2022 sans l'effet de la guerre en Ukraine, TC de IP 2108), ajustements statistiques 19, 20, 60 milliers. Naissances 2025 : 645 000, décès 651 000, solde naturel −6 000 (provisoire).
- Ajustements intercensitaires : −52 à −54 milliers/an (1990-1998), +94 455/an (1999-2005), puis rénovation du questionnaire 2018 et chocs (Covid, Ukraine) de 2015 à 2022 : à intégrer dans l'identité comptable (colonne « ajustement »).

## 7. Projections IP 2108 (`9004289`, 08/06/2026)

✅ 27 scénarios (3 composantes × 3 niveaux, PDF) ; le tableur n'en publie que 9 pour la population totale (Fig. 3) : central, fécondité basse / haute, espérance de vie basse / haute, solde migratoire bas / haut, population basse / haute.
Hypothèses (tableau complémentaire) : ICF 1,56 en 2025 → 1,45 dès 2028 (bas 1,20, haut 1,70 dès 2030) ; solde migratoire 150 000/an (bas 70 000 ; haut 230 000) dès 2026 ; espérance de vie 2070 : 89,5 (F) et 86,7 (H) ans.
Population (millions) : 2026 69,082 ; 2037 69,768 (pic, central) ; 2070 : central 65,887, migration basse 60,933, migration haute 70,841, fécondité basse 61,328 / haute 70,836 (scénarios population basse / haute : colonnes non lues). Pyramide 2026/2070 (Fig. 4, âge simple, H/F, central seul). **Aucune projection par origine** (U16 confirmé).

## 8. Registre U1-U16 : confirmations et corrections

- **U1 ✅** : le solde migratoire est « mesuré indirectement par différence » ; il reflète aussi l'aléa de sondage et de collecte. À ajouter : des ajustements statistiques entrent dans l'identité.
- **U2 ✅** : sorties d'immigrés estimées à 26 000 en 2022 ; avant : 65 à 125 milliers en 2014-2021 (71 à 109 en 2006-2013).
- **U3 ✅** avec précision : soldes et sorties connus jusqu'en 2022 ; entrées jusqu'en 2024 ; population immigrée jusqu'en 2025 (provisoire) ; recensement définitif 2023.
- **U4 corrigé** : pas d'enquête annuelle de recensement en 2021 ; les sources divergent sur les années réajustées (IP 2107 : 2019, 2020, 2021 et 2023 ; note de rupture : 2019 à 2022 ; fichier `2381757` : 2019 à 2023). L'entrée 2020 est estimée à partir de l'enquête Emploi.
- **U5 ✅ et chiffrée** (voir §4) : 2024, avec un effet quantifié, pas seulement signalé.
- **U6 ✅ et précisée** : trois ruptures de champ (métropole → hors Mayotte 1990 → France 2014 ; logement ordinaire pour descendants et IP 1910 ; hors Mayotte pour le tableau des immigrés 2006-2013).
- **U11 ✅ côté Insee** : les entrées sont les personnes arrivées pour s'installer au moins un an (recensement, tous statuts confondus, irréguliers compris) ; pas de statistique de titres de séjour à l'Insee (🔎 à chercher auprès du ministère de l'Intérieur). La méthode a été rénovée (document de travail 2025-11).

## 9. Écarts avec les ordres de grandeur du cadrage

- Confirmés : 7 970 000 immigrés (11,6 %) ; 6 297 000 étrangers ; 3 336 000 Français par acquisition ; 26 000 sorties d'immigrés en 2022 ; solde migratoire immigrés 348 000 ;
  projections central +150 000, ICF 1,45, population en baisse après 2037, 61 à 71 millions en 2070.
- Écart : « 2010-2020 : +1,5 pt (8,6 % → 10,1 %) » : le tableur donne 8,5 % en 2010, 8,6 % en 2011 et 10,2 % en 2020 (+1,6 à +1,7 pt) ; 10,1 % n'y figure pas. « 1920 : 3,7 % → 6,6 % » ✅ (1921 → 1931).
- Écart : la population hors Mayotte et les champs changent : population 2022 = 68 060 207 (France) et non les 65,8 M de la métropole (`FM`).
- Pas de DGEF ni de titres de séjour dans les données Insee. Pas de série Saphir 1968-1999 annuelle (🔎) : seuls les 5 recensements.
- Pas de G3 hors 0-59 ans et pas de série temporelle de descendants ; le chiffre de l'IP 1910 (G2 + G3) date de 2019-2020.

## 10. Questions à poser à Max

1. Piscine 2006-2022 : accepter d'abord un historique « mesuré » sur 17 ans, avec 1968-2005 en mode « reconstruit par stocks » (hypothèse de mortalité affichée) ?
2. Les « sorties » d'immigrés 2022 (26 000) cassent la tendance : lissage sur 3 à 5 ans, ou affichage brut avec alerte ?
3. Pour B2, une famille de pays plus fine (Pologne, Belgique, Italie seule) justifie-t-elle de chercher IMMFRA12 / fichiers détail du recensement ?
4. Tolérer le périmètre mixte (métropole avant 1990, France entière après) ou ne commencer la piscine qu'à 1990 ?
