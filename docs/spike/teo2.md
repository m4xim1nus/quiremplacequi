# Spike sources : générations, mixité et inégalités (TeO2 et Insee)

Vérifié le 2026-11-05. Source principale : *Trajectoires et Origines 2*
(Beauchemin, Ichou, Simon (dir.), Ined Éditions, 2026), lu dans le markdown
du wiki de Max (texte intégral des chapitres) ; **les tableaux et figures y
sont des JPEG**, téléchargés depuis OpenEdition et lus à la main
(`data/raw/spike/teo2/chNN/`, non versionnés). Compléments Insee :
`data/raw/spike/teo2/insee/` (xlsx lus par `docs/spike/scripts/teo2/xlsx_dump.py`).

Légende : ✅ vérifié dans le texte source ; 🔎 non trouvé ou non vérifiable ;
**[T]** chiffre dans le texte mais pas dans un tableau ; **[F≈]** lu sur un
graphique sans étiquettes (précision ± 0,5 pt).

## 0. Citer et réutiliser

- Page du livre : `https://books.openedition.org/ined/26527` (accès ouvert
  « freemium » : lecture en ligne libre ; PDF et ePub réservés aux
  bibliothèques ; publié le 19 mai 2026 ; ISBN 978-2-7332-9087-3).
- Chapitres : 5 `/ined/26345` ; 7 `/ined/26359` ; 8 `/ined/26366` ; 9
  `/ined/26373` ; 11 `/ined/26387` ; 16 `/ined/26422` ; 17 `/ined/26429` ;
  conclusion `/ined/26513`. Pagination : ch. 5 p. 123-140 ; ch. 7 p. 161-182 ;
  ch. 8 p. 183-204 ; ch. 9 p. 205-222 ; ch. 11 p. 249-272 ; ch. 16 p. 353-374 ;
  ch. 17 p. 377-392 ; conclusion p. 581-592. Le markdown n'a pas la pagination
  par figure : je cite le **numéro de paragraphe** (« §5 »).
- Licence : « Le texte seul est utilisable sous licence OpenEdition Books.
  Les autres éléments (illustrations, fichiers annexes) sont tous droits
  réservés ». Ressaisir des chiffres est possible ; **ne pas republier les
  images** de tableaux ou de figures.
- Champ de tout TeO2 : 18-59 ans, France métropolitaine, logement ordinaire,
  2019-2020 (sauf ch. 5 : 18-49 ans pour la comparaison TeO1/TeO2).

## 1. Inventaire chiffré (priorité 1)

### E1 : barre des générations (ch. 8)

| Chiffre | Valeur | Référence | |
|---|---|---|---|
| G1 / G2 / G3 / « sans ascendance immigrée sur trois générations » | **13 / 11 / 10 / 66 %** | ch. 8, §5 et tableau 1 « Lien à la migration de la population sur trois générations » (effectifs non pondérés 10 396 / 8 305 / 776 / 7 704 ; N = 27 181) | ✅ |
| G2 : deux parents immigrés / G2.5 (un parent) | 6 % / 5 % | tableau 1 | ✅ |
| G3 : « de deux à quatre grands-parents immigrés » / « G3.5 d'un grand-parent immigré » | 4 % / 5 % (somme 9, arrondi pour 10) | tableau 1 | ✅ |
| Dans les « 66 % » : natifs des Outre-mer 1, descendants de natifs des Outre-mer 1, Français de l'étranger 1, descendants de Français de l'étranger 4 | | tableau 1 (les Français de l'ancien empire colonial sont dans « Français de l'étranger ») | ✅ |
| « Un tiers de la population… a un lien à l'immigration sur trois générations » | 13 + 11 + 10 = 34 | ch. 8, §5 | ✅ |
| **41 %** « lien à l'immigration » (personnel, par ascendance ou par alliance) | 41 % | ch. 8, §19 et §42 ; conclusion générale, §2 et §21 | ✅ **[T]** |
| Définition du 41 % | regroupe G1 et natifs des Outre-mer, G2 et descendants d'Ultramarins, G3, **et les G4+ dont le conjoint est G1, G2, G3 ou ultramarin** | ch. 8, note 6 | ✅ |
| Génération par classe d'âge (7 classes × 6 colonnes) | ex. 18-24 ans : 7 / 7 / 8 / 4 / 5 / 68 ; 35-39 ans : 16 / 7 / 5 / 5 / 4 / 65 | ch. 8, tableau 2 « Liens à l'immigration… par classe d'âges » | ✅ |
| Immigrés < 25 ans ; < 18 ans ; 60+ | 7 % ; < 3 % ; 9 % | ch. 8, §8 (hors champ TeO2 pour < 18 et 60+) | ✅ **[T]** |

### E2 : mixité conjugale (ch. 8, ch. 7)

Tableau 3 du ch. 8 « Type de mixité d'union… selon le lien à la migration (%) »
(champ : personnes en couple, 18-59 ans). Colonnes : (a) même origine et même
lien ; (b) même origine, lien différent ; (c) conjoint G1 d'une autre origine ;
(d) conjoint G2 d'une autre origine ; (e) conjoint majoritaire.

| | (a) | (b) | (c) | (d) | (e) |
|---|---|---|---|---|---|
| G1 | 53 | 8 | 7 | 3 | **29** |
| G2 (deux parents immigrés) | 20 | 22 | 9 | 5 | **45** |
| G2.5 (un parent immigré) | 5 | 5 | 11 | 5 | **74** |
| Population majoritaire | – | – | 5 | 7 | **88** |
| Ensemble | 12 | 7 | 2 | 2 | 76 |

- **Les « 39 / 59 / 90 % » ne sont pas publiés** : ce sont des sommes
  (c + d + e : G1 7 + 3 + 29 = 39 ; G2 9 + 5 + 45 = 59 ; G2.5 11 + 5 + 74 = 90),
  « union avec un partenaire d'origine différente ». Seuls (e) = 29 / 45 / 74 et
  « 12 % des majoritaires en couple avec G1/G2 » (5 + 7, ch. 8 §18) sont lus tels quels.
  Texte : G1 « 11 % avec un G2 » et « 29 % avec une personne de la population
  majoritaire » (§17) ✅ **[T]**. Conclusion générale §2 : « 30 % des immigrés en union »,
  « 58 % des descendants », « 5 % de la population majoritaire en couple avec
  un conjoint immigré », « 7 % … de deuxième génération » ✅ (arrondis différents).
- Homogamie par lien : 78 % (calcul « hors tableau », note 5) ; homogamie lien + origine :
  20 % pour les G2, 5 % pour les G2.5 (§18) ✅ **[T]**.
- Ch. 7, figures 3 et 4 « Origine du conjoint » (hommes / femmes × origine, 4 modalités :
  immigré·e de même origine / descendant·e de même origine / immigré·e ou descendant·e d'une
  autre origine / Français·e sur deux générations). Exemples **[étiquettes lisibles]** :
  G1 ensemble, hommes 45 / 9 / 14 / 32, femmes 40 / 5 / 14 / 40 ; G2 ensemble,
  hommes 10 / 13 / 14 / 63, femmes 15 / 11 / 17 / 57 ; G2 d'un parent immigré hommes 3 / 6 / 13 / 78 ;
  Maghreb G2 hommes 23 / 17 / 15 / 45. ✅ Champ **différent** du ch. 8 : pour les immigrés, seulement
  ceux qui ont rencontré leur conjoint après la migration (ch. 7, §4) ; « natifs »
  = Français sur deux générations. Ne pas mélanger avec le tableau 3 du ch. 8.
- Ch. 8, §42 : « 11 % des G2.5 sont en union avec un·e immigré·e » (= colonne c seule) alors que
  §17 donne 16 % (b + c) ; incohérence interne mineure.

### E3 : généalogies des G3 (ch. 8)

| Chiffre | Valeur | Référence | |
|---|---|---|---|
| Nombre de grands-parents immigrés, G3 adultes (1 / 2 / 3 / 4) | **56 / 37 / 3 / 4 %** ; « 93 % en ont un ou deux » | ch. 8, §22 et tableau 4 (N = 778) | ✅ |
| Idem si ≥ 1 grand-parent immigré non européen | 49 / 37 / 5 / 9 % (N = 269, enquête complémentaire TeO2-G3) | tableau 4 | ✅ |
| Origine des G3 (18-59) : Maghreb 6, Afrique subsaharienne 2, Asie 2, Europe du Sud **56**, autres UE 27 27, autres pays 7 | | ch. 8, figure 1 (barres G1 / G2 / G3 étiquetées ; G1 : 32 / 20 / 7 / 9 / 11 / 9 / 13 ; G2 : 38 / 9 / 4 / 5 / 32 / 7 / 4) | ✅ |
| Génération par origine (part G1 / G2 / G3) | Europe du Sud 14 / 35 / 51 ; Maghreb 46 / 48 / 6 ; Afrique sub. 67 / 29 / 5 | ch. 8, figure 2 et §14-15 | ✅ |
| Parents immigrés de même pays (G2) | 90 % (annexe 2) ; G3 enfants : 88 % | ch. 8, §20 et §35 | ✅ **[T]** (annexes non lues) |
| Enfants des répondants (base enfants, N = 40 905) | G2 deux parents 8, G2 un parent 11, G3 7 + 5, majoritaires 66 ; 0-5 ans : 11 / 15 / 8 / 5 / 60 | ch. 8, tableau 5 | ✅ |
| G3 de la base enfants : 1 / 2 / 3 / 4 grands-parents immigrés | 44 / 40 / 5 / 12 % ; 4 grands-parents : Turquie-MO 41, Afrique sub. 33, Maghreb 24 | ch. 8, §37 et tableau 6 (N = 7 943 ; effectif Maghreb et Europe du Sud tous deux « 2 532 » : coquille probable) | ✅ |
| Lignage : 37 % des G3 à deux grands-parents les ont dans la même branche | | ch. 8, §38 | ✅ |

Chiffres du cadrage retrouvés **dans l'Insee** (IP 1910), pas dans TeO2 : « 5 % des G3 de 18-59 ans
ont quatre grands-parents immigrés, 20 % pour l'origine maghrébine » (feuille `Figure 3a`) ;
« 58 % des G3 de 18-59 ans ont ≥ 1 grand-parent né en Espagne, Italie ou Portugal » (même feuille) ✅.
Ch. 8 mesure autre chose : 4 % et « 56 % d'ascendance majoritaire Europe du Sud ».

### B5 : ce qu'il reste d'une vague

- IP 1910 `Figure 3a` (xlsx, G3 par origine d'au moins un grand-parent, 0-17 et 18-59 ans) ✅.
  `Figure 2a` à `2c` : origine géographique de G1, G2 (un et deux parents), G3 **par classe d'âge de
  5 ans, de 0 à 80+** ✅ : directement exploitable.
- « Les G2 de 60 ans et plus sont à 91 % d'origine européenne » : 🔎 absent de TeO2 (hors champ,
  18-59 ans). À recalculer depuis les colonnes 60+ de `Figure 2b1` d'IP 1910 si elles existent.
- TeO2 : les 55-59 ans G2 sont à plus de 50 % d'Europe du Sud, contre 15 % des 18-24 ans (ch. 8 §13) ✅ **[T]**.
- Part des G3 qui sont d'origine européenne : 83 % (UE 27) ; « moins de 14 % des originaires d'Europe
  du Sud sont immigrés » (§14) ✅.

### E9 : inégalités

**Sur-chômage à profil égal** (ch. 11, figure 1 « Risques nets de chômage chez les actifs… (effets
marginaux par rapport à la population majoritaire) », points de pourcentage, 16 groupes × 2 sexes,
**intervalles de confiance, pas d'étiquettes [F≈]**). Lecture : hommes G1 Maghreb ≈ +6, G2 Maghreb ≈ +6,
G2 Afrique sub. ≈ +6 ; femmes G1 Maghreb ≈ **+11,7**, G2 Maghreb ≈ +6, G2 Afrique sub. ≈ +5,7, G1 Turquie-MO ≈ +10.
Donc « +6 à +11,7 » est une lecture de graphique, cohérente, mais :
- **Contradiction texte/figure** : la conclusion du ch. 11 (§35) écrit « hommes immigrés d'Afrique du Nord
  +11 points, descendants +7 ; femmes +4 et +6 », alors que la figure 1 donne ≈ +6 / +6 pour les hommes et
  ≈ +11,7 / +6 pour les femmes (hommes et femmes semblent inversés dans le texte). À signaler, ne pas citer §35.
- Taux bruts : hommes 27 % (descendants d'Afrique sub.) contre 9 % (majoritaires), femmes 25 % (immigrées du
  Maghreb) contre 9 % (immigrées d'Europe du Sud) (ch. 11, §9, « hors tableau ») ✅ **[T]**.

**Ségrégation** (ch. 5, tableau 1, champ 18-49 ans, 2008 et 2019, « proportion d'individus résidant dans un
quartier du quintile supérieur » par Iris). Le « 36 / 51 % contre 6 % » du cadrage est :
indicateur *forte concentration d'immigrés non européens*, 2019, **Maghreb G1 + G2 = 36 %, Afrique sub. G1 + G2 = 51 %,
population majoritaire = 6 %** ✅. Indicateur « immigrés » : 33 / 47 / 6 ; G1 32, G2 25. Chômage du quartier : Maghreb 31, Afrique sub. 33,
majoritaires 10. Cadres : 19 / 18 contre 19. Attention : ce sont des **G1 et G2 mélangés** et un champ 18-49 ans ;
l'écart se creuse entre 2008 et 2019 (ch. 5 §10-11 et §16) ✅.
Ch. 5 §23 : à la G3, la plupart des différences disparaissent « sauf pour la proportion d'immigrés et le taux
de chômage » du quartier chez les G3 non européens (effectifs faibles).

**Discriminations déclarées** (ch. 16) ✅ :
- Tableau 2 « Discriminations situationnelles / autodéclarées / au moins un type » (champ 18-59 ans, 5 dernières années).
  Autodéclarées : majoritaires **14 %** ; G1 24 ; G2 29 ; G2.5 20 ; G1 Maghreb 25 ; G1 Afrique sub. 35 ;
  **G2 Maghreb 35 ; G2 Afrique sub. 41** ; G2 Europe du Sud 12 ; G2 Autres UE 27 15. « Au moins un type » : 25 % (majoritaires)
  à 52 % (G2 Afrique sub.).
- Tableau 1 : 18 % de l'ensemble (3 % souvent + 14 % parfois), motif origine 31 % des déclarants.
  G3 non européens (N = 172) : 2 + 19 = **21 %** contre 15 % (3 + 12) pour les majoritaires (reprise en conclusion générale, §18).
- Le « 14 % » est aussi le taux **de 2008** pour l'ensemble (18 % en 2020, ch. 16 §3 et §22) : ne pas confondre.
- Tableau 3 : expérience du racisme 41 % des G2 contre 27 % des G1 et 16 % des majoritaires.

### E10 : le paradoxe intégration / exposition

- Identification (ch. 9, tableau 4, champ descendants et originaires des Outre-mer 18-59 ans) : « France seule » **G1 15, G2 39
  (deux parents) / 48 (G2 total) , G2.5 58, G3 75, majoritaires 78** ✅ (les 39 % du cadrage sont les G2 à deux parents) ;
  « combinaison France + autre pays » 17 / 33 / 23 / 9 / 3. G3 : « 14 % évoquent un pays autre que la France » (§32).
- « Se sentir français : 71 / 94 / 98 / 97 % » : 🔎 introuvable dans les chapitres 9, 19, 21 et 24 (pas dans les textes fournis).
- Exposition : discriminations déclarées G2 29 % contre G1 24 % (ch. 16, tableau 2), racisme G2 41 % contre G1 27 % (tableau 3) ;
  déni de francité G1 / G2 / G2.5 : total 36 / 29 / 10 % (ch. 9, figure 3, étiquettes lisibles) ✅.
- « Plus intégrés ET plus exposés que leurs parents » n'est **pas une phrase du livre** : c'est la lecture de ces deux séries
  (voir §5 pour la formulation des auteurs).

### F2 : voir §4. Fécondité : voir §3.

## 2. Données derrière les figures

- **Pas de tableur compagnon** sur OpenEdition (« aucun xlsx ou csv »), ni lien vers un fichier de données ; la page de l'Ined
  `…/donnees-detaillees-enquete…teo2-disponibles-en-ligne/` et `teo.site.ined.fr` n'ont pas pu être lues (503 / DNS) : 🔎.
- Seul le **jeu de données Insee IP 1910** est un vrai tableur (`https://insee.fr/fr/statistiques/fichier/6468640/ip1910.xlsx`, 12 feuilles,
  chargé et lu ✅). Il couvre 0 à 80+ ans (enquête Emploi 2019-2020 pour G1 et G2, TeO2 pour les G3 de 18-59 ans), ce qui évite
  une partie de la saisie manuelle.
- **Saisie manuelle estimée** (valeurs étiquetées, une référence par cellule : « ch. N, tableau/figure X, ligne, colonne ») :

| Module | Sources à saisir | Cellules |
|---|---|---|
| E1 | ch. 8 tableaux 1 et 2 | ≈ 70 (tableau 2 = 54) |
| E2 | ch. 8 tableau 3 ; ch. 7 figures 3 et 4 (option) | 25 ; +168 |
| E3 / B5 | ch. 8 tableaux 4-6, figures 1-2 (IP 1910 en xlsx pour l'âge) | ≈ 130 |
| E9 | ch. 5 tableau 1 (88) ; ch. 16 tableaux 1-2 (≈ 130) ; ch. 11 figure 1 (≈ 32 points **sans étiquettes**) | ≈ 250 |
| E10 | ch. 9 tableau 4 et figure 3 (≈ 100) ; ch. 16 tableau 3 (≈ 80, option) | ≈ 100 à 180 |
| F2 | ch. 8 tableaux 1 + IP 1910 `Figure 1` (xlsx) | ≈ 20 |
| **Total** | | **≈ 600 sans options, ≈ 900 avec** |

Les valeurs lues sur graphique sans étiquettes (ch. 11 figures 1 et 3, ch. 5 figures 1 à 3) sont à marquer
« approx. » dans le fichier de données.

## 3. Paramètres de la piscine

**Besoins du modèle de cohortes** (âge × génération × origine agrégée) et ce qui existe.

| Paramètre | Source | État |
|---|---|---|
| Structure par âge de G1, G2 (un / deux parents), G3, majoritaires, 0-59 ans par classe de 5 ans (+ 60+ pour G1 / G2) | **IP 1910 `Figure 1`** (xlsx) ; ex. 0-4 ans : G1 0,8 ; G2 deux parents 13,3 ; G2 un parent 11,3 ; G3 14,0 ; autres 60,6 | ✅ |
| Origine agrégée par génération et âge | IP 1910 `Figures 2a-2c` (xlsx) ; TeO2 ch. 8 figure 1 | ✅ |
| Part des unions mixtes par génération (partenaire majoritaire) | TeO2 ch. 8 tableau 3 : 29 / 45 / 74 / 88 ; IP 1910 `Figure 4` : G1 27 %, G2 66 % (80 un parent, 50 deux parents) | ✅ (deux sources, deux champs) |
| Mixité par origine agrégée | IP 1910 `Figure 4` (10 origines × G1 / G2, xlsx) ; ch. 7 figures 3-4 | ✅ |
| Part des enfants nés de couples mixtes | TeO2 ch. 8 tableau 5 : parmi les enfants de 0-5 ans des répondants, G2 un parent 15 %, deux parents 11 %, G3 13 %, sans ascendance 60 % ; ch. 8 §21 (parent non immigré descendant d'immigrés dans 1/4 des cas) | ✅ pour 0-17 ; pas de série par cohorte de naissance |
| Naissances selon nationalité / pays de naissance des parents | Insee `https://www.insee.fr/fr/statistiques/2381382` (xlsx `demo-naiss-natio-pays-2.xlsx`, 1998-2025 ; 71,7 % de naissances de deux parents français en 2025) : **existe, lu par une autre personne** | ✅ existence |
| Fécondité par génération | ch. 17 §10-14 : descendance finale des femmes nées 1960-1974 : G1 **2,32**, majoritaires **1,87**, G2 **1,87** (deux parents 1,92 ; couple mixte 1,81) ; familles de 4+ enfants : G1 19 %, majoritaires 6 % ; Maghreb G1 33 % contre G2 11 % | ✅ **[T]** (figure 1 en images) |
| Taux de natalité par origine (ICF) | Reynaud 2023a (Population & Sociétés / Insee), cité par ch. 17 : 🔎 non lu ; le « ICF 2,3 des femmes nées à l'étranger (2021) » du cadrage n'est pas dans ch. 17 | 🔎 |

Limite importante : la convergence de fécondité « dès la G2 » vaut pour les **femmes nées avant 1975**,
dont les G2 viennent surtout d'immigrations européennes ; les auteurs le regrettent (ch. 17 §36 : « peu d'entre elles
sont issues des vagues d'immigration les plus récentes »). La convergence pour les G2 Afrique / Asie est donc **observée
partiellement** (4+ enfants : Maghreb G2 11 % contre 33 % en G1, ch. 17 §23). C'est un paramètre à mettre en fourchette.

**Liste minimale proposée** : (1) structure par âge × génération 2019-2020 (IP 1910 `Figure 1`) ;
(2) origine agrégée par génération et âge (`Figures 2a-2c`) ; (3) matrice de mixité par génération du parent et origine
(IP 1910 `Figure 4` + ch. 8 tableau 3) ; (4) part des enfants à un parent immigré / deux parents (ch. 8 tableau 5) ;
(5) fécondité par génération (ch. 17) et naissances Insee 2381382 pour caler les flux ; (6) règle de classement des enfants
(un parent immigré = G2 prioritaire sur G3, ch. 8 §27 ; origine du G2 à deux parents : père, ch. 24). Manque : taux de mixité
**de la génération des petits-enfants** (pas de projection publiée) ; les unions des G3 ne sont pas décrites.

**IP 1910 : xlsx confirmé** (`https://insee.fr/fr/statistiques/fichier/6468640/ip1910.xlsx`, 59 Ko). Champ : métropole, logement
ordinaire, 0-59 ans pour les G3 ; G3 mesurable seulement < 60 ans (feuille `Figure 1`, note) ✅.

## 4. F2 : le curseur de définition

Calculable à partir de chiffres **publiés** (additions simples), avec deux champs :

| Définition | 18-59 ans, TeO2 (ch. 8 tableau 1) | 0-59 ans, Insee (IP 1910 `Figure 1`, ligne 0-59) | Tous âges (IP 1910, ligne « Ensemble ») |
|---|---|---|---|
| G1 | 13 | 9,1 | 9,2 |
| G1 + G2 deux parents | 13 + 6 = 19 | 9,1 + 7,1 = 16,2 | 9,2 + 5,9 = 15,1 |
| G1 + G2 | 24 | 9,1 + 7,1 + 6,3 = 22,5 | 20,9 |
| + G3 (≥ 1 grand-parent immigré) | 34 (« un tiers ») | 32,7 | non mesurable (> 59 ans) |
| + conjoints, etc. | **41** (publié, note 6) | 🔎 non publié | |

- Publié : tous les chiffres du tableau 1, le 41 %, et la ligne IP 1910. **Reconstitué** : les sommes
  ci-dessus ; la ligne « G1 + G2 deux parents » est une somme ; la décomposition du 41 (34 + 7) aussi.
- Le 41 % **ne se décompose pas** en 34 + conjoints : il compte aussi les Ultramarins (G1 : 1 %, G2 : 1 %) ; il reste
  donc ≈ 5 points de G4+ en couple lié (41 − 34 − 2), reconstitué. La synthèse du wiki (« ~8 points ») est à corriger.
  Note : ch. 8 (note 6) parle de la **conjointe ou du conjoint** ; la conclusion générale §2 dit « par une union ou par sa propre descendance »
  (formulation plus large que celle du ch. 8) : 🔎 trancher avec le texte de l'annexe.
- Étendue : de 13 % à 41 % = ×3,2 ; 9,1 % à 32,7 % (0-59 ans) = ×3,6 ; pas de ×4 publié.
- **Chevauchement** : le chevauchement « ≥ 1 grand-parent français de France » (≈ 80 %, wiki) reste un calcul à
  hypothèses (cf. réserves de la synthèse `teo2-mythe-deux-blocs.md`) ; il n'est pas publié.
- Écart G1 TeO2 (13 %) / enquête Emploi (11,9 % à 18-59 ans) : les deux sources ne se mélangent pas dans une même barre.
- Pour un curseur réel « selon qui l'on compte » sur toute la population (tous âges), il manque les G3 de 60 ans et plus.

## 5. La nuance honnête : passages exacts

1. Ch. 8, §43 (Conclusion, p. 204) ✅ : « Il est encore trop tôt pour savoir si les immigrations postcoloniales suivront la même dynamique
   démographique. On identifie à ce stade plus de lignées homogènes pour les petits-enfants des immigré·es du Maghreb, d'Afrique subsaharienne
   et de Turquie et Moyen-Orient. » Et juste avant : « La dynamique d'incorporation dans le groupe majoritaire est perceptible pour les
   descendant·es des migrations européennes de l'entre-deux-guerres ». **Seul passage avec « trop tôt »** (chap. 9 et 16 ne l'emploient pas).
2. Ch. 9, §39 (Conclusion) ✅ : « seul·es les descendant·es d'immigré·es européen·nes suivent le modèle assimilationniste attendu en prenant leur
   distance avec les origines de leurs parents et en bénéficiant d'une forme d'invisibilité » ; « Ce maintien de la saillance des origines s'éclaire
   par l'expérience d'altérisation : le renvoi aux origines et les assignations (probablement stigmatisantes) contribuent à construire les identités
   ethnoraciales et religieuses. » Prudence des auteurs : « la causalité … est toutefois difficile à établir » (§26) et « l'inverse est également possible » ; ces
   formulations ne sont pas « entretenue par les discriminations » telle quelle (le mot est de la synthèse du wiki). Ch. 9, §40 : forte appartenance
   à la France « contrariée par des assignations stigmatisantes ».
3. Ch. 16, §34 (Conclusion) ✅ : « les discriminations ethnoraciales et le racisme restent structurants dans le vécu des Ultramarins, des Subsahariens
   et des Maghrébins » ; « les discriminations perçues ne sont pas des représentations gouvernées par les seuls affects, mais semblent s'enraciner
   dans la réalité socioéconomique ».
4. Conclusion générale, §20-21 ✅ : « Ces deux indicateurs d'altérisation renforcent la saillance des identités ethnoraciales » ; « La grande différence
   entre la séquence actuelle et celles du passé tient au contexte des migrations post-coloniales » ; « La persistance des discriminations explique en
   partie ces trajectoires clivées ».
5. Ch. 8, §43 : les auteurs précisent que Richard Alba insiste sur l'absorption dans la *whiteness* tandis qu'eux voient « la profonde hybridation de la
   population majoritaire » : à citer avec le « trop tôt », pas pour affirmer l'assimilation.

## 6. Microdonnées

- **Deux voies** (page Insee `…/metadonnees/source/operation/s2086/acces-micro-donnees`, lue) ✅ : (1) **Quetelet-Progedo Diffusion**, fichier de
  production et de recherche (FPR) « avec un niveau de détail supérieur » au fichier tout public, pour la recherche ; (2) **CASD**, fichiers individuels
  complets « sous réserve de l'accord du Comité du secret statistique ». Organismes publics : FPR « sous certaines conditions ».
  Une recherche annonce ~220 demandes validées, et un communiqué de l'Ined de février 2024 la mise à disposition : 🔎 non vérifié à la source.
- 🔎 **Délais, éligibilité d'un projet citoyen / journalistique, tarifs** : non trouvés (pages Ined et Progedo injoignables). À demander à
  Quetelet-Progedo et au CASD ; la conclusion générale (§23) parle de « base de données accessible à la communauté scientifique », ce qui laisse
  planer un doute pour un site grand public.
- **Apport** : pour la piscine, taux de mixité par cohorte de naissance et par origine fine, structure par âge et par origine des G3, fécondité des
  G2 jeunes (hors cohorte ≤ 1974) ; pour F2, un vrai calcul « selon qui l'on compte » avec intervalles et la déclinaison par origine ;
  pour E9-E10, des écarts non lus sur graphique. Limites : TeO2 ne permet pas les G3 > 59 ans ; la diffusion de résultats dérivés est encadrée ;
  les publications du site doivent être des agrégats non identifiants.

## 7. Écarts avec les ordres de grandeur du cadrage

| Sujet | Cadrage | Lu | Remarque |
|---|---|---|---|
| E1 | 13 / 11 / 10 / 66 ; 41 % | identiques (tableau 1 ; note 6) | le 41 % inclut les Ultramarins ; pas « 34 + 8 » mais ≈ 34 + 2 + 5 |
| E2 « 39 / 59 / 90 % » | présentés comme des taux | **sommes** de (c + d + e) du tableau 3 | seul (e) = 29 / 45 / 74 est publié ; ch. 7 donne d'autres valeurs (champ différent) |
| E3 « 9 sur 10 ont ≥ 2 grands-parents non immigrés » | | 93 % ont un ou deux grands-parents immigrés (ch. 8 §22) ; **56 % n'en ont qu'un** | équivalent ; 5 % (quatre GP) et 20 % (Maghreb) viennent d'IP 1910, pas de TeO2 (4 %) |
| B5 « 58 % des G3 ont un GP né en ESP / ITA / POR » | | confirmé dans IP 1910 (`Figure 3a`) ; TeO2 donne 56 % d'ascendance majoritaire Europe du Sud | deux mesures distinctes |
| B5 « G2 de 60+ : 91 % européens » | | 🔎 non lisible dans TeO2 (hors champ) | |
| E9 sur-chômage « +6 à +11,7 » | | cohérent avec la figure 1 ch. 11 [F≈] ; texte §35 incohérent (+11 / +7 hommes, +4 / +6 femmes) | |
| E9 discriminations « 14 % (majoritaires) à 35-41 % (G2) » | | ✅ tableau 2 ch. 16 (G2 Maghreb 35, G2 Afrique sub. 41) | le 14 % est aussi le taux global de 2008 |
| E9 ségrégation « 36 / 51 % contre 6 % » | | ✅ ch. 5 tableau 1 (G1 + G2, 18-49 ans, 2019) | champ 18-49 ans et G1 + G2 mélangés |
| E10 / E5 « se sentir français 71 / 94 / 98 / 97 % » | | 🔎 non trouvé | « France seule » ✅ |
| F2 « du simple au quadruple » | | ×3,2 (18-59 ans) à ×3,6 (0-59 ans) | |
| E7 « ICF 2,3 » | | ch. 17 : descendance finale **2,32** (G1, nées 1960-74), pas un ICF | |
| Nuance honnête | « trop tôt » attendu aux ch. 8, 9 et 16 | « trop tôt » **seulement ch. 8 §43** | ch. 9 : prudence causale ; ch. 16 : pas de formule |
