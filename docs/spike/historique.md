# Spike sources : le temps long (1851 → 1968) et les vagues migratoires

Vérifié les 2026-11-04 et 2026-11-05. Les valeurs ✅ ont été lues par script
(`docs/spike/scripts/historique/`) sur les fichiers de `data/raw/spike/historique/`
(non versionnés), ou lues sur la page citée avec sa référence. 🔎 = non trouvé ou non
vérifiable depuis ce poste. Réseau : Gallica (403), Numdam/EuDML (connexion coupée) et
le site de l'Ined (HTML anti-robot) n'ont pas pu être interrogés ; les chiffres
pré-1911 viennent donc de sources secondaires.

Scripts : `lire_xlsx.py`, `lire_pdf.py` (dump), `b1_b3_calculs.py` (B1 et B3),
`b2_nationalites.py` (B2), `pdf_vecteurs.py` et `fig1_numerisation.py` (numérisation du
graphique vectoriel).

## 1. Tableau des jeux

| Jeu / source | Contenu | Période | Format | Verdict | Remarques |
|---|---|---|---|---|---|
| Insee, *Population immigrée et étrangère* [`/2381757`](https://www.insee.fr/fr/statistiques/2381757), xlsx `demo-etran-part-pop-etran-immig.xlsx` | immigrés (effectif, part) ; Français de naissance, Français par acquisition, étrangers | 1921 → 2025 (années de recensement avant 2006, annuel ensuite) | xlsx, 2 feuilles | **OK, colonne vertébrale** | Rupture de série en 2024. Pas de nationalité. |
| Insee Réf. 2023, [`/6793226`](https://www.insee.fr/fr/statistiques/6793226), xlsx `IMMFRA23-F2.xlsx` | fig. 1 : immigrés **depuis 1911** ; fig. 2 : immigrés par grande zone / pays de naissance | 1911 → 2021 ; 1968, 75, 82, 90, 99, 2006, 10, 21 | xlsx | **OK, mais agrégé** | « Espagne, Italie » **cumulés** ; « Maroc, Tunisie » cumulés ; **Pologne absente**. Erratum du 24/05/2024 (Amérique classée à tort en Europe avant 2000). |
| Insee Réf. 2012 (IMMFRA12), fiche 1.2 « Histoire de l'immigration » [`/1374019`](https://www.insee.fr/fr/statistiques/1374019), p. 6, fig. 1 | **table croisée** lieu de naissance × nationalité (6 colonnes + immigrés) | 1911 → 2008 | PDF texte (extractible) | **OK** | Seule source tabulaire des « Français par acquisition » nés à l'étranger avant 1968. ~16 lignes × 8 colonnes, déjà lues par script. |
| Insee Réf. 2005 (IMMFRA05) [`/1371777`](https://www.insee.fr/fr/statistiques/fichier/1371777/IMMFRA05.PDF), fiche 1.6, p. 13 | même table, 1911 → 1999, avec la note sur les Algériens | 1911 → 1999 | PDF texte | OK | Valeurs identiques à la fiche 2012 jusqu'en 1982. |
| Insee Réf. 2012, **Vue d'ensemble** [`/1374014`](https://www.insee.fr/fr/statistiques/1374014), `IMMFRA12_b_VE_posfra.pdf` | fig. 1 : ‰ de la population par nationalité, **1851 → 2008** (25 recensements) ; fig. 2 : étrangers par nationalité, milliers, 1946 → 2008 ; fig. 5 : immigrés rétropolés dès 1846 | 1851 → 2008 | **graphique vectoriel dans un PDF, aucune table** | **partiel** | Le PDF de grdr.org est **identique octet pour octet** à l'original Insee (`cmp`). Pas de tableur associé sur les pages Insee 1374013 / 1374014 / 1374019 (le seul lien « fichier » est le PDF). |
| Insee Première 1910 [`/6468640`](https://www.insee.fr/fr/statistiques/6468640), xlsx `ip1910.xlsx`, feuilles « Encadré Figure a/b/c » | **part (%) de la population** de chaque nationalité : Belges, Espagnols, Italiens, Polonais, Portugais (1901 → 2020) ; Algériens, Marocains, Tunisiens, autres Afrique (1946 → 2020) ; Turcs, Indochine (1946 → 2020) | 1901 → 2020 | xlsx | **OK, la seule table par nationalité** | Arrondi à 0,1 point (≈ ± 20 000 personnes en 1931) : suffisant pour des courbes, pas pour des effectifs. |
| Insee Première 2011 [`/8236359`](https://www.insee.fr/fr/statistiques/8236359), `ip2011.xlsx` | immigrés nés en Europe par pays de naissance, 2023 | 2023 | xlsx | OK pour B5 | « IP 2011 » est le **numéro** de l'Insee Première (29/08/2024, P. Tanneau), pas une année. |
| Rygiel 2010 (HAL `halshs-00548192`), p. 4-5 | étrangers par nationalité, données SGF | 1851, 1891, 1911 | PDF texte | secondaire, ✅ lu | Total 379 289 / 1 130 211 / 1 159 835. Reproduit le tableau de la SGF sans le localiser (🔎 volume exact). |
| SGF, *Résultats statistiques du recensement général*, Gallica | tableaux d'origine par nationalité | 1851 → 1936 | scans | 🔎 **inaccessible ici** | À consulter en navigateur. Meuriot, « La population étrangère en France (1851-1911) », *JSFS* 53 (1912), p. 555 (Numdam `JSFS_1912__53__555_0`) est la synthèse contemporaine la plus prometteuse (🔎 non téléchargée). |
| Annuaires statistiques rétrospectifs (Insee), Mauco 1932 | séries par nationalité 1851 → 1936 | | scans | 🔎 | Non localisés en version numérique accessible. |

**Réponse à la question 1 (B1).** Il n'existe **pas de tableur** pour la série par
nationalité 1851 → 1911 ; il existe une **table** pour les totaux (étrangers, immigrés,
naturalisés) de 1911 à nos jours, et un **graphique vectoriel** pour 1851 → 1906.

### Série de totaux, valeurs lues (`b1_b3_calculs.py`)

| Recensement | Étrangers (k) | Part | Immigrés (k) | Part | Français par acquisition (k) |
|---|---|---|---|---|---|
| 1851 | 379 (Rygiel) | ≈ 1 % | 🔎 | | |
| 1891 | 1 130 (Rygiel) | 🔎 | 🔎 | | |
| 1911 | 1 160 (table 2012) | 3,0 % (calculé) | 1 110 | 2,8 % | 168 nés à l'étranger + 85 nés en France |
| 1921 | 1 532 | 3,9 % | 1 429 | 3,7 % | 254 |
| 1926 | 2 409 | 6,0 % | 2 288 | 5,7 % | 249 |
| 1931 | 2 715 | 6,6 % | 2 729 | 6,6 % | 361 |
| 1936 | 2 198 | 5,3 % | 2 326 | 5,6 % | 517 |
| 1946 | 1 744 | 4,4 % | 1 986 | 5,0 % | 853 |
| 1954 | 1 765 | 4,1 % | 2 293 | 5,4 % | 1 068 |
| 1962 | 2 151 | 4,6 % | 2 861 | 6,2 % | 1 267 |
| 1968 | 2 621 | 5,3 % | 3 238 | 6,5 % | 1 320 |

(Insee `2381757`, sauf 1911 : table 2012. Champ : France métropolitaine jusqu'en 1982.)

**Raccord avec 2381757.** Les recoupements sont exacts : immigrés 1921, 1931, 1946, 1962
identiques entre 2381757, `IMMFRA23-F2.xlsx` et la table 2012 ; étrangers 1931 = 2 714 k
(table, somme des colonnes) contre 2 714,7 k (2381757) ; 1962 = 2 151 k contre 2 150,6 k.
**Écart connu en 1968** : 3 281 k immigrés dans la table 2012 (et 3 281 dans IMMFRA05)
contre 3 238 k dans 2381757 et `IMMFRA23-F2`, soit 43 k (révision de l'exploitation
Saphir). Les étrangers 1968 valent 2 664 k (table) contre 2 621 k (2381757). Retenir la
série **2381757 + IMMFRA23-F2**, la plus récente. La table 2012 apporte la décomposition
Français par acquisition / étrangers pour les nés à l'étranger, à ne pas mélanger avec 2381757
sans noter la révision. **1911 n'est que dans IMMFRA23-F2 et la table 2012** (2381757
commence en 1921).

**Valeurs repères du concept (calculées).** Part des immigrés « devenus français » :
15,1 % en 1911, 8,9 % en 1926, 11,2 % en 1931, 27,8 % en 1946, **33,7 % en 1954**, 31,1 % en 1968.

## 2. B2 : tableau de disponibilité par vague

Concept : **E** = étrangers par nationalité (recensements) ; **I** = immigrés par pays de
naissance (Insee, 1968 →). Les deux ne se raccordent pas (voir §3).

| Vague | Années | Concept | Source exploitable | Précision |
|---|---|---|---|---|
| Belges | 1851, 1891, 1911 (effectifs) ; 1901 → 2020 (part %) | E | Rygiel 2010 ; IP 1910 encadré | effectifs ponctuels ; part à 0,1 pt |
| Italiens | idem + graphique 1851 → 2008 | E (puis I agrégé « Espagne, Italie » dès 1968) | idem ; Mourlane 2016 | voir repères |
| Espagnols, Portugais | 1851-1911 (Espagnols 29 736 / 77 736 / 105 760) ; part 1901 → 2020 ; I agrégé 1968 → 2021 | E puis I | Rygiel ; IP 1910 ; `6793226` | Portugais : I séparé seulement (282 k en 1968) |
| Polonais | part 1901 → 2020 ; 507 811 en 1931 | E | IP 1910 ; MNHI | pas dans `6793226` |
| Russes, Arméniens | 1851-1911 : « sujets russes » 9 338 / 14 357 / 35 016 ; après 1921 inclus dans « Autres Europe, y compris Russes » | E | Rygiel ; fig. 2 de la Vue d'ensemble | 🔎 pas de série Arméniens |
| Algériens | part 1946 → 2020 ; I : 378 k (1968) → 887 k (2021) | E (nationalité) puis I | IP 1910 encadré b ; `6793226` | piège §3 |
| Marocains, Tunisiens | part 1946 → 2020 ; I **cumulés** 219 k (1968) → 1 151 k (2021) | E puis I | idem | séparés en E, cumulés en I |
| Turcs | part 1975 → 2020 ; I : 43 k (1968) → 251 k (2021) | E puis I | IP 1910 encadré c ; `6793226` | |
| Afrique hors Maghreb, Asie | I dès 1968, détail depuis 2006 | I | `6793226` | |

**Repères vérifiés.**
- Italiens, recensement de 1931 : **808 000** (Mourlane, *Cahiers d'études italiennes* 22, 2016, p. 159-160, [openedition `cei/2938`](https://journals.openedition.org/cei/2938)) ; 2,0 % de la population dans IP 1910, soit 825 k à ± 20 k (compatible : 808 k = 1,96 %).
- Italiens en 1946 : **450 000** (Mourlane, p. 160), soit **− 44 % entre 1931 et 1946** (naturalisations et retours) ; IP 1910 donne 1,1 % (≈ 438 k). Remontée de 26,2 % de 1946 à 1968 selon la même source (≈ 568 k).
- Italiens au recensement de 1962 : **571 684**, 29 % des étrangers (Mourlane, p. 159).
- Polonais : 507 811 « âmes polonaises recensées » en 1931 (MNHI, *Polonia, synthèse historique*, note 3, p. 7) ; 422 000 en 1936 ; moins de 15 000 avant la guerre, près de 600 000 arrivés jusqu'au début des années 1930 (p. 5 du même document). IP 1910 : 1,2 % en 1931, soit 495 k, cohérent.
- Pics (IP 1910, calculés) : Belges 1921, Italiens et Polonais 1931, Espagnols 1968, Portugais 1975, Algériens 1982 (1,5 %).
- Graphique de la Vue d'ensemble, numérisé (`fig1_numerisation.py`, 3 courbes sur 5 retrouvées) : Italiens à 19,5 ‰ en 1931 brut, ≈ 19,9 ‰ après correction de l'écart de zéro de 0,4 ‰ (lecture imprimée : « 20 millièmes »), Belges à 12,5 ‰ brut en 1886 (≈ 12,9 ‰ corrigé), pic du XIXe siècle. Preuve que le vecteur est exploitable ; la précision est de ± 0,2 ‰, soit ± 8 000 personnes.

**Effort de saisie.** Pour une table par nationalité aux 21 recensements 1851 → 1968
(12 recensements d'avant 1914 + 1921, 26, 31, 36, 46, 54, 62, 68), sur ~12 nationalités :
**≈ 250 cellules**, à saisir depuis les volumes SGF (Gallica) ou Meuriot 1912 pour 1851-1911.
À la place, une extraction du graphique vectoriel couvre ~12 séries × 25 points = 300 valeurs,
automatisable, à ± 0,2 ‰.

## 3. Le piège des concepts (U9)

- **Étrangers ≠ immigrés.** En 1931 les deux se confondent (2 715 k contre 2 729 k) ;
  en 1954 l'écart est de **528 k** (1 765 k contre 2 293 k), parce que 773 k immigrés
  sont devenus français et 377 k Français sont nés à l'étranger. Un immigré naturalisé
  sort des étrangers sans quitter les immigrés (Insee Réf. 2012, p. 15-16 de la Vue d'ensemble).
- **Le stock de Français par acquisition** (2381757) est la seule série longue
  disponible en tableur : 254 k (1921) → 1 320 k (1968). Il mesure le stock, pas les flux.
- **Flux de naturalisations.** Aucune série annuelle 1851 → 1968 sous forme exploitable n'a
  été trouvée. Repères : 1 048 684 personnes ayant acquis la nationalité du 10 août 1927 à
  juillet 1940, dont 299 900 adultes et 348 050 mineurs naturalisés par décret, 249 481 par
  déclaration ou de plein droit, 56 500 par mariage (Zalc, *Dénaturalisés*, 2016, repris dans
  la présentation APHG du 15/10/2024, p. 8, [PDF](https://www.aphg.fr/IMG/pdf/aphg151024czalc.pdf)). Une source secondaire (Geneawiki, page « Naturalisation ») donne
  38 000 par an en moyenne de 1927 à 1938 et 81 000 en 1938 (🔎 non recoupé). Un immigré sur dix
  était naturalisé en 1881, un sur cinq en 1911 (Vue d'ensemble, p. 12, 🔎 à comparer aux 15,1 % calculés pour 1911).
  Sources primaires à explorer : *JSFS* 1904 (« La nationalité française, acquisitions et
  pertes de 1851 à 1902 », Numdam `JSFS_1904__45__112_0`, 🔎 inaccessible), Weil, *Qu'est-ce qu'un
  Français ?* (🔎 série annuelle non vue), Justice (acquisitions depuis 2001).
- **Algériens avant 1962.** La note de la table Insee (IMMFRA05, p. 13) dit que les originaires
  d'Algérie, « bien que juridiquement français et nés sur un territoire français avant 1962,
  sont comptés avec les étrangers nés à l'étranger », et que « de 1954 à 1968, ils ont été dénombrés
  comme musulmans algériens » ; les rapatriés français de naissance ne sont pas des immigrés.
  Conséquence : les « étrangers » de 1954 et 1962 d'Insee **contiennent déjà** les Algériens
  (IP 1910, encadré b : 0,5 % de la population en 1954, 0,8 % en 1962), alors que les
  recensements d'époque les comptaient à part. Ined (Kesztenbaum et Simon) : 335 000 musulmans
  algériens dénombrés au recensement du 7 mars 1962, jugés sous-évalués (350 000 à 450 000), méthode
  de reconnaissance onomastique — 🔎 cité par une recherche web, PDF Ined non lisible ici.
  **Écart à examiner** : Italiens 1962 = 29 % des étrangers (Mourlane) correspond à un total d'environ
  1,97 million, soit moins que les 2,15 millions d'Insee, ce qui est compatible avec une base
  sans les Algériens, mais je ne l'ai pas démontré.

## 4. U10 : migrations juives 1880-1939

La statistique ne dispose d'**aucune catégorie religieuse** : on ne peut passer que par les
nationalités (Pologne, Russie, Roumanie, Allemagne, Autriche). Les ordres de grandeur sourcés
trouvés sont minces et à confirmer dans les ouvrages :
- Épelbaum, *Les enfants de papier* (Grasset, 2002) : environ **100 000** Juifs polonais
  immigrés jusqu'en 1940 (notice du MNHI, [`juifs_polonais.pdf`](https://www.histoire-immigration.fr/sites/default/files/musee-numerique/documents/juifs_polonais.pdf), p. 2) ✅ lu, 🔎 page du livre.
- Pour Paris, des spécialistes estiment à ~70 000 les Juifs d'Europe orientale installés entre
  1918 et 1939, dont ~40 000 Polonais (🔎 résumé web, source exacte non identifiée).
- Les Juifs forment ~15 % de l'immigration polonaise (🔎 même résumé) ; la communauté polonaise
  de 1931 (507 811) contient donc une part juive non mesurée par le recensement.
- Dynamique : immigration « non organisée » de Juifs polonais fuyant l'antisémitisme à partir de
  1936-1937 (MNHI *Polonia*, p. 7) ; Lifshitz-Krams, *La naturalisation des Juifs en France au
  XIXe siècle* (CNRS, 2002) sur la période antérieure.
- Total de la population juive de France en 1939 : de 300 000 à 350 000 selon les sources
  web consultées (🔎 aucune n'est un historien de référence : Marrus-Paxton, Green, Benbassa,
  Hyman, Weinberg et Noiriel sont à lire directement).

**Verdict U10 : partiel.** Un encadré « ce que la statistique ne voit pas » est faisable
avec 2 à 3 ordres de grandeur d'historien à vérifier ; une série chiffrée ne l'est pas.

## 5. B3 : vitesse comparée des vagues (`b1_b3_calculs.py`)

| Période | Part | Variation | Stock immigrés |
|---|---|---|---|
| 1921 → 1931 | 3,7 % → 6,6 % | **+ 2,9 pt** | + 1 300 k |
| 1946 → 1954 | 5,0 % → 5,4 % | + 0,4 pt | + 307 k |
| 1962 → 1975 | 6,2 % → 7,4 % | + 1,2 pt (13 ans) | + 1 026 k |
| 2010 → 2020 | 8,5 % → 10,2 % | **+ 1,7 pt** | + 1 333 k |
| 2011 → 2021 | 8,6 % → 10,2 % | + 1,6 pt | + 1 327 k |
| 2015 → 2025 | 9,3 % → 11,6 % | + 2,3 pt (hors rupture 2024) | + 1 801 k |

**Le calcul se reproduit pour les années 1920 : + 2,9 points (confirmé par Insee Réf. 2023 `6793226`
et IP 1910).** Pour les années 2010, l'encadré d'IP 1910 donne « de 8,6 % à 10,1 % », soit + 1,5 point,
alors que la série actuelle 2381757 donne + 1,7 point entre 2010 et 2020 (8,5 → 10,2 %) et + 1,6
point entre 2011 et 2021. **En stock, la décennie 2010 (+ 1 333 k) égale celle des années 1920 (+ 1 300 k)** ;
seule la part rapportée à une population plus grande est moindre. À présenter avec ce double
indicateur, et avec la rupture de série de 2024 (+ 440 k d'immigrés entre 2023 et 2024).

## 6. B4 : frise des discours (repérage léger)

✅ = référence bibliographique vue dans une source consultée pendant ce spike ;
🔎 = référence à vérifier, lien Gallica non obtenu (403).

| Date | Jalon | Référence | Statut |
|---|---|---|---|
| 1870-1914 | xénophobie, « La France hostile » | L. Dornel, *La France hostile. Socio-histoire de la xénophobie (1870-1914)*, Hachette, 2004 | ✅ (cité par Mourlane, n. 7) |
| 1886 | Drumont, *La France juive*, Flammarion | notice BnF ; texte sur Gallica | 🔎 ark à retrouver |
| 1893 | Barrès, *Contre les étrangers* | — | 🔎 |
| 16-17 août 1893 | massacre d'Aigues-Mortes | G. Noiriel, *Le massacre des Italiens. Aigues-Mortes, 17 août 1893*, Fayard, 2010 | ✅ |
| 1895-96 | capitaine Danrit (É. Driant), *L'Invasion noire*, Flammarion | bibliothèque numérique de la Défense (copie numérisée) | ✅ notice, 🔎 date (1894 selon une source) |
| 1919-1939 | opinion et étrangers | R. Schor, *L'opinion française et les étrangers en France, 1919-1939*, Publications de la Sorbonne, 1985 | ✅ |
| 1931-1936 | renvois d'étrangers ; xénophobie liée à la crise | P. Rygiel, in Blévis-Zalc, *Les étrangers au temps de l'exposition coloniale*, Gallimard-CNHI, 2008, p. 72-73 (93 000 sorties en 1931, 108 000 en 1932) | ✅ |
| 1932 | Mauco, *Les étrangers en France*, Armand Colin | thèse de géographie | ✅ notice, 🔎 texte |
| 1961 | crainte d'une « invasion » italienne avec la libre circulation | Mourlane 2016, p. 169 | ✅ |
| 1973 | Raspail, *Le Camp des saints*, Laffont | — | 🔎 |
| 1985 | *Figaro Magazine*, « Serons-nous encore français dans trente ans ? » | couverture attestée par l'introduction de *Still French? France and the Challenge of Diversity, 1985-2015* | ✅ la question, 🔎 date et auteur |
| 2011 | R. Camus, *Le Grand Remplacement*, D. Reinharc | — | 🔎 |
| 2023 | LDH, *Droits & Libertés* n° 203 | sommaire non trouvé (le n° 202 est en ligne sur ldh-france.org) | 🔎 |

**Verdict B4 : partiel.** La frise tient sur 6 ouvrages d'historiens vérifiables ; les textes
primaires (Drumont, Barrès, Danrit, Figaro Magazine) sont à chercher à la main sur Gallica
(l'API est fermée aux outils en ligne de commande).

## 7. B5 : ce qu'il reste d'une vague

Insee Première 1910 (`ip1910.xlsx`, lu par script) :
- Figure 3a : **58 %** des descendants de 3e génération de 18 à 59 ans ont au moins un grand-parent
  immigré originaire d'Espagne, d'Italie ou du Portugal (41 % pour les moins de 18 ans) ✅.
- Texte : « au-delà de 60 ans, **91 %** [des descendants de 2e génération] sont d'origine européenne,
  avec parfois des migrations très anciennes (italienne, espagnole, polonaise, belge, allemande) » ✅.
- 5,8 millions d'immigrés (9 %), 7,5 millions de G2 (12 %), 4,8 millions de G3 de moins de 60 ans (10 %) ✅.
- G2 : 27 % ont un parent né en Espagne, Italie ou Portugal, 34 % au Maghreb (figure 3b) ✅.
- Les G3 sont **limités à moins de 60 ans** : les générations des vagues belge, polonaise et italienne
  de 1900-1930 sont invisibles (classées « sans ascendance migratoire directe »).

Insee Première 2011 (`ip2011.xlsx`, 2024) : 2,4 millions d'immigrés nés en Europe en 2023 (3,5 % de la
population), dont 25 % au Portugal ✅ ; détail à lire dans le xlsx.

**Verdict B5 : GO** pour une mise en regard vague → descendants, sans lien nominal entre les
vagues anciennes et les G3 actuels (la variable « grand-parent né en Pologne » n'est pas séparée).

## 8. Écarts avec les ordres de grandeur du cadrage

- Le tableur de « ‰ par nationalité 1851-2008 » n'existe pas : c'est un **graphique** (le PDF
  grdr.org est identique à l'original Insee). La table par nationalité n'existe qu'à partir de
  1901, en part arrondie (IP 1910).
- Immigrés 2025 : 7 970 000, 11,6 %, étrangers 6 297 400, Français par acquisition 3 335 700 ✅ cohérent.
- 808 000 Italiens en 1931 ✅. 
- B3 : « 2010-2020, + 1,5 pt (8,6 → 10,1 %) » est la lecture d'IP 1910 ; la série actuelle donne
  + 1,7 pt (8,5 → 10,2 %). Le calcul des années 1920 (+ 2,9 pt) est exact.
- « 58 % des G3 de 18-59 ans » ✅ ; « G2 de 60 ans et plus à 91 % d'origine européenne » ✅.
- « Un immigré sur dix naturalisé en 1881, un sur cinq en 1911 » (Vue d'ensemble, p. 12) :
  la table donne 15,1 % en 1911 (pas 20 %), l'ordre de grandeur est à nuancer.
- Italiens 1962 : 1,4 % de la population (IP 1910, soit 650 k) contre 571 684 au recensement
  (1,23 %, Mourlane) : écart de 14 %, probablement une erreur d'arrondi ou de champ dans l'encadré, à signaler.
- Polonais 1931 : 507 811 correspondent à 18,7 % des étrangers (2 714,7 k), et non 17,6 % comme
  l'écrit le MNHI (base ou champ différent).
- Immigrés 1968 : 3 281 k (Insee Réf. 2005 et 2012) contre 3 238 k (séries 2023 et 2381757).

## 9. Verdicts

| Module | Verdict | Motif |
|---|---|---|
| B1 totaux 1921 → 1968 | **GO** | tableur 2381757 et table 2012, recoupés |
| B1 avant 1921 | **partiel** | 1911 en tableau ; 1851, 1891 en totaux ; 1856-1906 sur graphique seulement |
| B2 par vague | **partiel** | table de parts 1901 → 2020 (IP 1910) ; effectifs par nationalité 1851-1911 à saisir ; pas de Pologne dans `6793226` |
| B3 | **GO** | calcul vérifié, à présenter en parts et en stocks |
| B4 | **partiel** | 6 références historiennes ✅, textes primaires 🔎 |
| B5 | **GO** | IP 1910 et IP 2011 |
