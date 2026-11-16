# Sources : verdict du spike

Version du 2026-11-05. Synthèse des quatre rapports de `docs/spike/` (le
détail, les URL et les scripts de lecture y sont). ✅ vérifié, 🔎 non trouvé.

## 1. Verdict par module de la v1

| Module | Verdict | Meilleure source | Limite principale |
|---|---|---|---|
| **A** Piscine, 4 vannes, immigrés et non-immigrés | **partiel** | Insee IP 2107 (`8998082`), bilans démographiques (`8999013`) | Les 4 vannes séparées n'existent que pour **2006-2022**. 2023-2024 : entrées seules. 1968-2005 : stocks de recensement et totaux seulement, flux net d'immigrés reconstructible, entrées et sorties non séparables. Décès d'immigrés **modélisés par l'Insee** (l'état civil ne les identifie pas). |
| A Robinet « naissances » par origine des parents | **GO** | Insee `2381382`, 1998-2025 | « Né à l'étranger » ≠ « immigré » ; rupture 2010-2011 ; depuis 2023, le second parent peut être une mère n'ayant pas accouché. |
| A Mixité et âge (pyramide vivante) | **GO** pour une photo 2019-2020 | Insee Première 1910 (`ip1910.xlsx`) : G1/G2/G3 par âge de 0 à 80 ans et plus, mixité par origine ; TeO2 ch. 8 et 17 | Pas de série temporelle ; pyramide fine des immigrés non publiée (4 classes d'âge ; fichiers détail du recensement à tester). |
| **B1** Série longue | **GO de 1911/1921 à 2025**, partiel avant | Insee `2381757` (dès 1921), `IMMFRA23-F2.xlsx` (dès 1911) | Avant 1911 : trois points (1851, 1891, 1911) via un historien. Rupture 2024 chiffrée dans la note Insee (+198 000 immigrés corrigés, contre +440 000 apparents). |
| **B2** Vague par vague | **partiel** | Encadré d'IP 1910 : parts par nationalité 1901-2020 (Belges, Espagnols, Italiens, Polonais, Portugais ; Maghreb et Turcs dès 1946) ; `2381755` (2006-2025) | Parts arrondies à 0,1 point ; regroupements grossiers après 1968 (Espagne + Italie, Maroc + Tunisie, pas de Pologne). Effectifs fins : ≈ 250 cellules SGF à saisir. |
| B3 Vitesse des vagues | **GO** | B1 | Années 1920 : +2,9 points ; années 2010 : +1,7 point ; en stock, les deux décennies se valent (≈ +1,3 million). |
| **B5** Ce qu'il reste d'une vague | **GO** | IP 1910 | 58 % des G3 de 18-59 ans ont un grand-parent venu d'Espagne, d'Italie ou du Portugal ; 91 % des G2 de 60 ans et plus sont d'origine européenne. |
| **E1** Trois générations | **GO** | TeO2 ch. 8, tableaux 1-2 | Champ 18-59 ans, métropole ; tableaux en image : saisie. |
| **E2** Mixité conjugale | **GO** | TeO2 ch. 8, tableau 3 | Les « 39 / 59 / 90 % » sont des sommes de colonnes, à présenter comme telles. |
| **E3** Généalogies | **GO** | TeO2 ch. 8, tableaux 4 et 6 ; IP 1910 fig. 3a | Deux sources pour « quatre grands-parents immigrés » (TeO2 4 %, IP 1910 5 %). |
| **E9** Inégalités | **GO, avec précautions** | TeO2 ch. 5 (ségrégation), 11 (chômage), 16 (discriminations) | Sur-chômage lu sur une figure sans étiquettes (± 0,5 point) ; ségrégation sur les 18-49 ans. |
| **E10** Le paradoxe | **partiel** | TeO2 ch. 9 (tableau 4), 16 | « Se sentir français 71 / 94 / 98 / 97 % » introuvable ; le paradoxe est une lecture croisée, pas une phrase du livre. |
| **F2** Curseur de définition | **GO** | TeO2 ch. 8 tableau 1 (18-59 ans) ; IP 1910 fig. 1 (0-59 ans) ; descendants 2025 (`4186761`) | De 13 % à 41 % : rapport ×3,2, pas ×4. Le 41 % inclut les originaires des outre-mer. Pas de G3 au-delà de 60 ans. |

**Hors v1, repérés** : B4 (13 jalons de discours, textes primaires à
retrouver sur Gallica), projections IP 2108 (27 scénarios, 9 publiées en
tableur, aucune par origine), microdonnées TeO2 (Quetelet-Progedo ou CASD).

## 2. Formats et accès

- **Insee** : xlsx sous Licence Ouverte 2.0, téléchargeables par `curl`.
  L'API BDM (SDMX) répond **sans clé** pour les séries de population,
  naissances et décès, mais n'a rien sur les immigrés : le pipeline lira les
  xlsx.
- **TeO2** : tous les tableaux et figures sont des **images**. Pas de
  tableur compagnon ; illustrations « tous droits réservés » : on ressaisit
  les chiffres, on ne republie pas les images. Saisie estimée à ≈ 600
  cellules pour E1-E3, E9-E10 et F2, une référence par cellule. IP 1910 en
  xlsx en couvre une partie.
- **Séries historiques** : la courbe des ‰ par nationalité 1851-2008 n'existe
  qu'en graphique vectoriel (numérisable à ± 0,2 ‰). Les volumes SGF
  (Gallica) et Meuriot 1912 (Numdam) étaient injoignables par script.

## 3. Conséquences pour la piscine

1. **2006-2022 est la période « mesurée »** : 4 vannes, immigrés et
   non-immigrés, identité vérifiée à ± 1 000 près (exemple 2022 : 375 000
   entrées − 26 000 sorties − 71 000 décès = +278 000 immigrés).
2. **1968-2005 est reconstruite** : stocks de recensement, décès d'immigrés
   estimés (rapport décès / stock calé sur 2006-2022, entre 0,98 et 1,12),
   flux net par différence. La vanne des arrivées et celle des départs
   fusionnent en une vanne nette, explicitement marquée.
3. **Les sorties sont fragiles** (U2) : 26 000 en 2022, contre 65 000 à
   125 000 les années précédentes. Il faut les lisser ou les afficher avec
   une alerte.
4. **L'âge et la mixité** viennent d'une photo 2019-2020 (IP 1910, TeO2) :
   la pyramide vivante est un modèle calé sur cette photo et sur les stocks
   de recensement, pas une série observée.
5. **La « piscine » n'est pas une image d'Héran** (aucune occurrence trouvée).
   Héran se méfie même des « mégaphores » aquatiques (cours du 3/12/2021). Le
   site l'assume donc comme sa propre image, et comme une **comptabilité**,
   pas une explication.

## 4. Écarts avec les ordres de grandeur de départ

Ce que le spike corrige (détail dans chaque rapport) :

- Part d'immigrés en 2010-2020 : de 8,5 % à 10,2 %, soit **+1,7 point** (et
  non 8,6 % → 10,1 %).
- Curseur de définition : de 13 % à 41 %, soit **×3,2**, pas « du simple au
  quadruple ».
- Les 39 / 59 / 90 % de couples mixtes sont des sommes ; le partenaire
  majoritaire seul donne 29 / 45 / 74 %.
- Discriminations déclarées des majoritaires : le chiffre de 14 % est aussi
  celui de 2008, à dater correctement.
- « ICF 2,3 des immigrées » : c'est une descendance finale (cohortes
  1960-1974 : 2,32 contre 1,87).
- « Grand renouvellement » : formule non retrouvée dans un texte d'Héran
  (seulement dans une note de lecture d'un tiers). Formules vérifiées :
  « infusion durable et non intrusion massive » (*Annuaire du Collège de
  France* 2017-18, p. 528), « on peut la réguler mais pas l'inverser » et
  « tout le contraire du grand remplacement » (diaporama ICM 2023, diapos 15
  et 14).
- Polémique de 2026 : la tribune du *Monde* (11 mai) est collective (ICM) ;
  l'article du *Figaro* (9 juin) porte sur l'Ined, pas sur les graphiques ; le
  texte du fact-check AFP reste introuvable.
- Le tableur « ‰ par nationalité 1851-2008 » n'existe pas.

## 5. Décisions (Max, 2026-11-05)

- **Piscine avant 2006** : reconstruite et marquée. Stocks de recensement +
  décès d'immigrés estimés (hypothèse calée sur 2006-2022, affichée) ; une
  vanne nette remplace les entrées et les sorties.
- **TeO2** : saisie référencée maintenant (≈ 600 cellules, une référence par
  cellule, relecture par script et par un agent indépendant). Microdonnées :
  piste pour plus tard.
- **Vagues (B2)** : les parts d'IP 1910 d'abord (Belges, Italiens, Polonais,
  Espagnols, Portugais, Maghreb, Turcs), précision de 0,1 point affichée.
  Migrations juives : encadré qualitatif sourcé chez les historiens. Saisie
  SGF au backlog.
- **Note OID du 21/9/2026** : réponse en v1 par le curseur de définition (F2)
  et un encadré en version forte ; contre-projection au cycle 2.

Par défaut (règles du cadrage, non reposées) : sorties d'immigrés en moyenne
pluriannuelle avec les valeurs annuelles en pointillés (U2) ; axes à zéro
pour les niveaux, toute troncature signalée.

## 6. Cycle 2 : l'espace et la nature des migrations (2026-11-16)

Spike court, fait en même temps que le pipeline (`pipeline/qrq/sources.py`).

| Famille | Accès | Ce qui est pris | Limites |
|---|---|---|---|
| Ministère de l'Intérieur (DSED) | ✅ data.gouv.fr (`static.data.gouv.fr`), CSV ; le site du ministère refuse les scripts (403) | Premiers titres par motif : série publiée le 27 juin 2024 (2011-2023, hors Britanniques) et fichiers annuels définitifs publiés en août 2026 (2015-2024, par motif, sous-motif et nationalité) | Pas de série avant 2011 à champ constant : la publication de juin 2019 (2007-2018) ne couvre que la métropole, en `.xls` ; non retenue. Cellules « nc » (secret) déduites du total du motif |
| Eurostat | ✅ API SDMX 2.1, SDMX-CSV | `demo_gind` (population, taux naturel, migratoire y c. ajustement, croissance), `migr_pop3ctb` (pays de naissance), `migr_asyappctza` (demandes), `migr_asydcfsta` (décisions de 1re instance), `nama_10_gdp` (PIB) | Solde migratoire = croissance − naturel (U22) ; Royaume-Uni absent après 2019 |
| OCDE | ✅ API SDMX (`sdmx.oecd.org`) | Entrées standardisées à titre permanent par catégorie (`DF_MIG_INT_PER`, 2014-2025) ; population historique (`DF_POP_HIST`) | Catégories harmonisées, sans étudiants ni temporaires (U23) ; stocks de nés à l'étranger (`DF_MIG_POPF`) incohérents pour la France en 2000 : non retenus |
| ONU (*International Migrant Stock* 2024) | ❌ 403 aux scripts | — | C7 (bosse migratoire) et l'émigration subsaharienne reportés |
| Elipa 2 (*Infos Migrations* n° 98) | ❌ site du ministère, 403 | — | U7 non enrichie |

**Raccord des titres** : de 2015 à 2022, total de la série de 2024 + Britanniques
= total du fichier annuel, à l'unité près (`qrq check`). 2023 : révision du
provisoire au définitif de 1,1 %.

**Témoins** : le livre d'Héran (3e éd., 2021) donne, pour 2017, 261 000
entrées d'immigrés ; l'export (IP 2107) en donne 291 000. Les entrées sont
révisées à chaque millésime ; le livre n'est pas un témoin utilisable. Ses
rangs pour l'asile (France 14e des demandes par habitant sur 2014-2020) sont
de même ordre que ceux du site (15e sur 2015-2025), sans être comparables
(période, pays).

**Décisions prises en autonomie** (à relire par Max) : noms des pages
(« Les arrivées », « Ailleurs ») ; D6 (lois sur la courbe des titres) renvoyé
à B4, comme les jalons de lois refusés sur la piscine ; Britanniques séparés
(accord de retrait retiré des motifs, total « hors Britanniques » tracé) ;
période de l'asile = onze dernières années publiées ; entrées OCDE en moyenne
sur dix ans, catégories secondaires absentes comptées zéro.
