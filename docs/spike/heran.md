# Spike sources — le corpus de François Héran

Date du relevé : novembre 2026. Légende : ✅ vérifié dans le document cité ; 🔎 non trouvé ou non vérifiable (source secondaire, accès bloqué).
Fichiers téléchargés : `data/raw/spike/heran/` (PDF + `.txt` extraits ; PNG des diapos consultées). Scripts : `docs/spike/scripts/heran/` (`extract.py`, `render.py`).

Abréviations. **ICM** = diaporama *Vérités et contrevérités sur l'immigration*, 63 diapos, 2/11/2023 (`icm.pdf`). **AFD** = *Pour débattre sur les migrations. Quelques données à connaître*, 30 diapos, 18/12/2025 (`afd.pdf`). **30Q** = *Parlons immigration en 30 questions*. **Annuaire** = *Annuaire du Collège de France*. **Note OID** = F. Héran, « Observatoire de l'immigration et de la démographie : la malmesure des migrations… », 12 mai 2026 (`gc/note_heran_oid.pdf`). **GC** = F. Héran, « L'Ined et la démographie en péril, ou le mythe du fossoyeur », *La Grande Conversation*, 2 juillet 2026 (`gc/gc_oid.pdf`).
Modules du site : A piscine · B temps long · C espace · D nature des migrations · E générations et mixité · F demain · G rhétorique et perceptions. Jugements : **R** reproduire tel quel · **M** mettre à jour · **A** améliorer · **X** hors sujet.

---

## 1. Catalogue de graphiques

### 1.1 ICM, 2/11/2023 (✅ lu en texte, puis en image pour les diapos 7, 9, 17, 25, 32)

Source : <https://icmigrations.cnrs.fr/wp-content/uploads/2023/11/Immigration-et-projet-de-loi-Darmanin_Verites-contreverites_Heran-02-11-2023.pdf>. Sur 63 diapos, une vingtaine contiennent un graphique ; le reste est du texte argumentatif ou politique (projet de loi Darmanin, CEDH).

| Diapo | Ce qu'elle montre / forme | Donnée et source citées | Geste | Mod. | Jugement |
|---|---|---|---|---|---|
| 6 | Définition de l'indicateur : « le meilleur indicateur est la part des immigrés dans la population, résultante des entrées, des sorties et des décès » ; G2 comptée à part. Texte. | Recensement depuis 1851, annuel depuis 2006 ; Enquête Emploi | H2, H3 | A | R (en légende de la piscine) |
| 7 | Nombre absolu (millions) et part (%) d'immigrés depuis 1851 : deux courbes sur **deux axes** (% à gauche, millions à droite), points datés, trou 1936-1946. | Recensements SGF et Insee « étrangers + naturalisés » ; 0,9 % (1851), 6,6 % (1931), 7,4 % (1975), 10,3 % (2021) ; 7,0 M | H2, H4 | B1 | M (2024 : 11,3 %, 7,7 M selon Note OID p. 23-24) et A (axe double, ruptures de définition à annoter) |
| 8 | Zoom 1970-2021 avec bandes de présidents (Chirac, Sarkozy, Hollande, Macron) ; hausse « quels que soient les présidents ». | Insee ; recensement tournant annuel depuis 2006 | H8 | B1 | M ; reprendre l'overlay de mandats et de lois |
| 9 | % d'immigrés dans les pays européens depuis 2000, par groupes de pays (courbes à 5 points). Axe 0-20 %. | ONU, *International Migrant Stock* 2020, définition large (y c. rapatriés) ; France 13,1 % en 2020 | H1, H3, H4 | C1 | M (version 2024 = AFD 17) ; ajouter le toggle de définition |
| 10 | Progression relative du nombre d'immigrés depuis 2000 : monde +62 % (173 → 281 M), Europe, France ; « +59 % » stricto sensu pour la France. | ONU | H4, H8 | C2 | M (AFD 18 : +74 / +105 / +50 %) |
| 12 | Part de la population née à l'étranger dans l'UE au 1/1/2021 ; barres classées ; France « en position moyenne ». | Eurostat | H1, H3 | C1 | M |
| 13 | Cinq facteurs de la hausse depuis 2000 (études, conflits, pays mi-chemin, économie/famille, climat « guère constaté »). Texte. | Base IDMC (déplacés internes) | H10 | D | R (texte) |
| 14 | Générations : G1+G2 = 24 % des adultes ; 31 % avec les petits-enfants ; **5 %** ont 4 grands-parents immigrés (20 % pour le Maghreb). Texte seul, aucun graphique. | TeO2 (Insee-Ined, 2019) | H12 | E1, E3 | A (en faire une barre ; réconcilier avec 41 % de GC p. 8) |
| 15 | Double conclusion : « on peut la réguler mais pas l'inverser » ; progression linéaire ; 21 lois depuis 1993. Texte. | — | H8, H9 | B | R |
| 17 | **Premiers titres de séjour ≥ 1 an, adultes de pays tiers, 2005-2022** : six petits multiples (étudiants, familles de Français, familles d'étrangers, réfugiés/malades, travail, autres), barres + total ; bandeau de présidences. Chaque panneau a **sa propre échelle verticale**. | DGEF (ministère de l'Intérieur) ; 193 000 → 311 000 ; 8 % d'étrangers malades en 2022 | H5, H9 | D1 | M (AFD 23 prolonge jusqu'à 2024 : 326 000) et A (échelle commune, version « pour 10 000 hab. ») |
| 18 | Décomposition de la hausse 2005-2022 (+61 %) : 50 % études, 27 % travail, 15 % refuge ; familial −3 %. Texte et chiffres. | DGEF | H5 | D1 | A (cascade / waterfall à construire) |
| 19 | Pourquoi ne pas ajouter asile et entrées illégales aux titres : doubles comptes (40 % des demandeurs obtiennent un titre). Texte. | — | H6 | D3, G1 | R |
| 20 | Détail des titres familiaux 2007-2022 : barres empilées ; regroupement stricto sensu ≈ 12 000/an ; VPF dont 40 % entrés depuis ≥ 9 ans (ELIPA). | DGEF ; enquête ELIPA | H5 | D2 | M (2022 « pas encore disponible » à l'époque) |
| 21 | Migration familiale (85 000/an) ≠ regroupement familial (12-14 000/an). Texte. | DGEF | H5 | D2 | R |
| 23 | Principe : chiffres relatifs (analogie Covid, sel pour 100 g, prix au m²). Texte. | — | H1 | transv. | R (c'est le toggle absolu/relatif) |
| 24 | Demandes d'asile UE + Royaume-Uni, 2013-2022, **pour 10 000 hab.** : ~30 courbes lissées (spaghetti). | Eurostat, UK Home Office | H1, H7 | C4 | A (illisible sans survol ; petits multiples ou classement interactif) |
| 25 | Même graphique annoté : Suède, Autriche, Allemagne, Grèce, Malte, Chypre ; accord UE-Turquie ; Covid. **Axe tronqué à 170** : la courbe de Chypre sort du cadre. | idem | H1, H7 | C4 | A ; défaut à ne pas reproduire vu la polémique de 2026 |
| 26 | Remarques : demandes ≠ décisions ; hypothèse « maximaliste » (tous les déboutés restent) ; « à aucun moment la France n'a été en 1re ou 2e ligne ». Texte. | — | H1, H7 | C4 | R (à recalculer sur 2013-2025) |
| 27, 28 | Décisions positives de protection pour 10 000 hab. depuis 10 ans (27) et détail 2018-2022 (28). Courbes/barres. | Eurostat | H1, H7 | C4 | M |
| 29 | 1res demandes d'asile en Europe en 2022 **par région d'origine, en absolu** (Allemagne 166 760 Proche/Moyen-Orient vs France 39 375, ×4,2). Barres par pays. | Eurostat | H1 | C4 | M |
| 30 | Idem **pour 10 000 hab.** (20 vs 5,8, ×3,5). Même mise en page que 29 : la paire absolu → relatif est la démonstration du toggle. | Eurostat | H1 | C4 | R (modèle de bascule) |
| 31 | Cumul 2013-2022 en absolu (Allemagne 1 545 140 vs France 183 390, ×8,4). | Eurostat | H1 | C4 | M |
| 32 | Cumul 2013-2022 **pour 10 000 hab.**, barres horizontales à bandes par région d'origine (Chypre 75,8 ; Autriche 58,2 ; Allemagne 20,0 ; France 5,8…). | Eurostat | H1 | C4 | A ; ✅ **anomalie** : les valeurs Allemagne 20,0 / France 5,8 et la phrase de lecture sont identiques à celles de la diapo 30 (année 2022 seule), alors que la diapo 31 donne un cumul décennal (≈ 186 pour 10 000 en Allemagne avec ~83 M d'hab., calcul de l'auteur de ce relevé). Probable copier-coller : ne pas reprendre ces chiffres sans recalcul. |
| 37 | Critères de la « part » de la France : 15,5 % de la population de l'UE, 17,8 % du PIB (Allemagne 19,0 / 26,0 %) ; variante EEE+Suisse. Tableau texte. | Eurostat | H7 | C5 | M |
| 38 | Parts prises par l'Allemagne et la France : demandes et relocalisations 2014-2020 + Ukrainiens 2022 ; Afghans 2022 : France 11 %, Allemagne 34 %. | Eurostat, UE | H7 | C5 | M |
| 39 | Réfugiés ukrainiens enregistrés pour 1 000 hab., fin 2022 : barres classées, trames « limitrophes » et « pays ennemis ». | non indiquée sur la diapo 🔎 | H1, H7 | C5 | M ; sourcer |
| 40 | Part des réfugiés ukrainiens vs part du PIB européen, ratio en barres, pointillés d'égalité ; « Géorgie : 4 fois sa part du PIB ». | idem | H7 | C5 | R (forme très lisible) |
| 41 | Si la France avait pris sa part : 360 000 protections temporaires (14 % de 2,55 M) contre 100 000 ; rôle des diasporas (Pologne 500 000, Italie 235 000…). Texte. | Eurostat 2020 | H7 | C5 | M |
| 42 | Hors Proche-Orient, la France enregistre 18 % des demandes UE = son poids dans le PIB. Texte. | Eurostat | H7 | C5 | M |
| 43 | Décisions positives pour 10 000 hab., pays d'Europe (diapo sans titre, image). | Eurostat | H1 | C4 | M |
| 44 | Lampedusa, « autoroute à péage aux barrières fermées sauf une » : effet de zoom. Analogie, pas de graphique. | — | H1 (variante) | G1 | R (ajouter au bestiaire) |
| 46-47 | Thèse de l'« appel d'air » : testée par les **préférences révélées** (répartition réelle des migrants), pas par la générosité des dispositifs ; IZA World of Labor 2014 (Giuletti). Texte. | — | nouveau (H20) | G | R |
| 49-50 | « Capacités d'accueil » structurelles (population, PIB) vs construites (décisions politiques). Texte. | — | nouveau (H21) | G | R |
| 22, 33-36, 45, 48, 51-62 | Cadrage, conclusions, projet de loi Darmanin, régularisations, CEDH art. 8, mirage danois. | — | — | — | X (daté ; le mirage danois et la CEDH relèvent d'un autre site) |

### 1.2 AFD, 18/12/2025 (✅ texte et images des diapos 4-8, 10, 13-15, 18, 23, 25, 30)

Source : <https://grdr.org/IMG/pdf/afd_paris_heran_18-12-2025.pdf>. Sur 30 diapos : 19 graphiques, 4 de cadrage.

| Diapo | Ce qu'elle montre / forme | Donnée et source citées | Geste | Mod. | Jugement |
|---|---|---|---|---|---|
| 2, 3 | Couvertures : H. de Haas, *How Migration Really Works* (Penguin, 2024) ; S.-A. Bisiaux (dir.), Éd. de l'Atelier, 2025. | — | H13 | G | X (références) |
| 4 | **Corpus de 206 publications « n idées reçues »** : tableau par type d'émetteur (associations 102 = 50 %, université 51, médias 33, org. internationales 11, gouvernements 9) + courbe annuelle 1990-2025 (≈ 35 en 2024). 7 langues. | Recensement de l'auteur, oct. 2025, « article pour *Maux d'exil* » | H13 | G3 | R (idée), 🔎 corpus non publié (voir §6) |
| 5 | **Les 30 idées reçues les plus fréquentes** (fréquences 119 → 15) : délinquance 119, « prennent le travail » 111, coût 110 ; invasion/submersion 52 ; grand remplacement 47 ; âge inédit des migrations 45 ; « l'un des pays les plus attractifs » 15. Tableau. | idem | H13 | G3 | R (sommaire du module G) |
| 6 | Dix recommandations du projet BRIDGES (H2020, CIDOB) sur les récits. Photo d'un diaporama. | BRIDGES | H13 | G | X (utile pour le ton éditorial) |
| 7, 8 | Opinion publique : barres 100 % empilées ; 60 % « trop d'immigrés », 28 % « ce qu'il faut », 4 % « trop peu » ; plus nuancé selon le motif (vie meilleure : 48 % moins ; fuyant la guerre : 31 % moins, 23 % plus). | Focaldata, **Royaume-Uni**, 1 009 adultes, *Financial Times*, 29/9/2023 | H14 | G2 | M (remplacer par un sondage français, ex. IFOP avril 2026 cité par l'OID) |
| 10 | Pays dont la part d'immigrés dépasse 11 % en 2024, par régions du monde : barres classées ; **France 17e d'Europe occidentale** (14 %). | ONU IMS 2024 | H1, H3, H4 | C1 | R (très bon) ; A : le seuil de 11 % est un choix à justifier |
| 11-13 | **« Bosse migratoire »** : nuage log-log taux d'émigrés × PIB/hab., cercles ∝ population (11 = mode d'emploi, 12 = nuage, 13 = schéma par zones). | ONU IMS 2024 ; taux = émigrés / (pop. + émigrés) | H10 | C7 | A (log-log peu lisible : annoter les zones comme en 13) |
| 14, 15 | Taux d'émigrés par pays, barres horizontales par groupe (« insécurité » : Guyana 36 %, Venezuela 23 % ; « guerre » : Palestine 44 %, Syrie 27 % ; Balkans : Bosnie 34 %). | idem | H10 | C7 | R (complément du nuage) |
| 16 | « Deux vérités » : la migration progresse partout, et en France à un rythme moindre ; citations de B. Retailleau (16/10/2024) et F. Bayrou (« submersion migratoire », 27/1/2025). Texte. | Eurostat, OCDE, ONU | H8 | C, G | R |
| 17 | Évolution du % d'immigrés en Europe 2000-2024, par groupes. Courbes. | ONU IMS 2024 | H3, H4 | C1 | R |
| 18 | **Progression relative du nombre d'immigrés 2000-2024, base 0 en 2000** : monde +74 %, EEE+ +105 %, France +50 %, Europe orientale −26 %, Europe du Sud +203 % ; annotations « crise des réfugiés », « invasion de l'Ukraine ». | ONU IMS 2024 | H4, H8 | C2 | R ; A : l'indice masque les niveaux (effet de base), le montrer avec la diapo 17 |
| 19-20 | Commentaire (« poussée linéaire, continue, pas exponentielle ») ; reprise de la courbe 1851 de l'ICM 7. | recensements | H8 | B1 | M |
| 21 | Cinq facteurs de la hausse depuis 2000 (reformulé : économique « moins marquée », S. Rosière). Texte. | — | H10 | D | R |
| 22 | Approche par les titres : 340 000 titres + 160 000 demandes ≠ « un demi-million d'entrées » (doubles comptes, 40 %). Texte. | DGEF | H6 | D3, G1 | R ; vérifier 340 000 (le total de la diapo 23 est 326 000) |
| 23 | **Titres de séjour ≥ 1 an, pays tiers, 2005-2024 (provisoire)** : six petits multiples, absolu (milliers) ; total 326 000 en 2024 ; légende en quatre puces. | DGEF | H5 | D1 | R en forme ; A comme ICM 17 |
| 24 | Nouveaux immigrés en % de la population d'accueil, pays de l'OCDE, 2023. | OCDE | H1 | C3 | M |
| 25-29 | **Entrées par catégorie pour 10 000 hab., moyenne annuelle 2014-2023**, pays par pays : barres empilées (autres, libre circulation UE, humanitaire, familial, famille accompagnante, travail). Quatre planches (Allemagne et Suisse sur la 25). Échelle commune 0-160. | OCDE | H1, H5 | C3 | R (le graphique qui combine espace et nature) ; 🔎 source de la 27 mal légendée (« moyeze ») |
| 30 | **Demandeurs d'asile afghans pour 10 000 hab., 2010-2024**, barres annuelles en bandes par pays (Suède 43 en 2015, Autriche 29 et 28, Grèce 22, France quasi nulle). | Eurostat, rapproché des recensements | H1, H7 | C4 | R ; A (lisibilité des petites barres) |

---

## 2. Les questions de *Parlons immigration en 30 questions* → modules

✅ Sommaire lu dans l'extrait : <https://www.vie-publique.fr/files/2021-11/9782111573765_DEP_Actu_ParlonsImmigration_Extrait_0.pdf> (p. 2-3 de l'extrait). L'extrait ne contient que le *Panorama* (p. 7-27), pas les doubles pages de réponses. **Le sommaire compte 33 entrées** (pages 30 à 94, une double page chacune), pas 30. Panorama : « Allemagne, Espagne, France : trois logiques migratoires » = soldes naturel et migratoire comparés (module C6).

| N° | Question (page) | Module |
|---|---|---|
| 1 | Étranger, immigré : quelle différence ? (30) | transv. (glossaire, H3, curseur F2) |
| 2 | Combien d'immigrés en France ? (32) | B1, A |
| 3 | Combien de « secondes générations » ? (34) | E1 |
| 4 | Comment mesurer les flux migratoires ? (36) | A, D4 |
| 5 | Combien d'entrées en France chaque année ? (38) | D1 |
| 6 | Qu'y a-t-il dans le solde migratoire ? (40) | A (vannes), D5 |
| 7 | Entrer et séjourner dans l'UE, à quel titre ? (42) | D |
| 8 | Peut-on chiffrer l'immigration illégale ? (44) | D (incertitudes) |
| 9 | Depuis quand la France est-elle un pays d'immigration ? (46) | B1, B4 |
| 10 | D'où viennent les immigrés ? (48) | B2 |
| 11 | Où vivent aujourd'hui les immigrés ? (50) | C1 |
| 12 | Pourquoi migrer ? (52) | D, C7 |
| 13 | Migrations forcées ou migrations libres ? (54) | D |
| 14 | Le changement climatique déclenche-t-il des migrations ? (56) | D (hors v1) |
| 15 | Où vont les étudiants internationaux ? (58) | D1 |
| 16 | Peut-on quitter son pays pour s'établir où l'on veut ? (60) | hors périmètre (droit, éthique) |
| 17 | Demander l'asile : pourquoi, où, comment ? (62) | D3 |
| 18 | L'Europe, terre d'asile ? (64) | C4, C5 |
| 19 | Que donnerait l'ouverture des frontières ? (66) | hors périmètre (normatif) |
| 20 | L'Europe a-t-elle une politique migratoire commune ? (68) | hors périmètre |
| 21 | Droit du sang ou droit du sol ? (70) | hors périmètre (nationalité) |
| 22 | La France accepte-t-elle la double nationalité ? (72) | hors périmètre |
| 23 | Les « statistiques ethniques » sont-elles légales ? (74) | E (encadré méthode TeO2) |
| 24 | La France se passerait-elle des immigrés ? (76) | F |
| 25 | Peut-on prévoir les migrations ? (78) | F |
| 26 | Les Subsahariens en route vers l'Europe ? (80) | C, G (la « prophétie de la ruée ») |
| 27 | Sait-on ce que coûte l'immigration ? (82) | hors périmètre v1, mais à anticiper : terrain central de l'OID |
| 28 | La France serait-elle aussi féconde sans l'immigration ? (84) | E7, F3 |
| 29 | Quel sens au « grand remplacement » ? (86) | **A, E, F4, G** (question pivot) |
| 30 | La traite esclavagiste, une forme de migration ? (88) | hors périmètre (B marginal) |
| 31 | Le racisme peut-il être systémique ? (90) | E9 |
| 32 | Quels critères d'intégration ? (92) | E |
| 33 | L'intégration en panne ? (94) | E9, E10 |

Couverture : 24 questions sur 33 tombent dans A à G ; 9 hors périmètre (16, 19-22, 27, 30 et, selon le choix, 14 et 23). Les modules A et F (projections, piscine) n'ont **aucune question dédiée** dans le plan du livre : ils sont une valeur ajoutée du site.

---

## 3. *Annuaire du Collège de France* : cycles de la chaire

Pages de la chaire : <https://www.college-de-france.fr/fr/chaire/francois-heran-migrations-et-societes-chaire-statutaire/annual-summaries>. Seuls **cinq résumés** sont publiés (2017-18 à 2021-22). ✅ Les cycles suivants n'ont pas encore de résumé en ligne (🔎 celui de 2022-23 serait dans le volume 123 : introuvable à ce jour).

| Cycle | Résumé (OpenEdition / PDF) | Angles, arguments, graphiques mobilisés | Mod. |
|---|---|---|---|
| 2017-18, *Introduction à l'étude des migrations* | ✅ <https://journals.openedition.org/annuaire-cdf/15834>, p. 527-536. Leçon inaugurale du 5/4/2018 : quatre tensions ; **« infusion durable et non intrusion massive »** (p. 528) ; démenti de la métaphore des « vases communicants / trop-plein » ; « ce n'est pas la misère du monde qui s'invite chez nous mais la richesse émergente ». Cours 1 (1/6/2018) : Ngram Viewer, définition ONU de l'immigré. Cours 2 : ~20 graphiques listés (p. 530-531), dont stock mondial 1990-2017, flux 1846-1940, étrangers recensés depuis 1851, titres 2005-2017, soldes naturel/migratoire, décisions positives par million d'habitants 2016. Cours 3 : sondage Gallup, « migration potentielle » 14 % → 1,5 % prévoient de partir dans l'année → 0,5 % ont commencé les préparatifs (p. 532). | B, C |
| 2018-19, *Pourquoi migrer ?* | ✅ <https://journals.openedition.org/annuaire-cdf/17390>, p. 617-620 | Seuls les intitulés sont publiés : théories, distribution mondiale des flux et diasporas, préférences des migrants, « n'importe qui ne migre pas n'importe où », systèmes migratoires hors Occident. Publications : « Comment se fabrique un oracle : la prophétie de la ruée africaine sur l'Europe » (*La Vie des idées*, 2018) ; fécondité des immigrées (*Population et Sociétés* 568, 2019). | D |
| 2019-20, *Intégration : constats et débats* | ✅ <https://journals.openedition.org/annuaire-cdf/18597>, p. 485-488 | Intitulés seuls (10 cours : assimilation, droit de la citoyenneté « le sang, le sol, le temps », « spectre du communautarisme », « sort de la deuxième génération », indicateurs d'intégration). | E |
| 2020-21, *Les politiques migratoires de par le monde* | ✅ <https://journals.openedition.org/annuaire-cdf/19735>, p. 599-607 | **Cours 2, 6/11/2020** (voir ci-dessous). Cours 3-4 : *policy gap* (Hollifield), « paradoxe libéral », progression des titres depuis 2005, historique des lois ; cours 6 : mesure des discriminations. Cours 1 : franchissements de frontière ≈ 200 fois plus nombreux que les entrées de migrants. | B, F, D |
| 2021-22, *L'immigration en débat : rhétorique et arguments, disputes et polémiques* | ✅ <https://journals.openedition.org/annuaire-cdf/20637>, p. 635-642 | Cours 1 (29/10/2021) : série de graphiques (9 pays les plus peuplés : 1 % d'émigrés ; 5 premiers couloirs ; recensements depuis 1851 ; titres 2005-2020 ; asile depuis 1975). Cours 4-7 : pente glissante, « bon sens » vs statistique, jugement de folie, *reductio ad Hitlerum/Stalinem*, **métaphores et « mégaphores »** (cours 5, 3/12/2021), réversibilité. | G |
| 2022-23, *Les migrations à la lumière du droit* | 🔎 résumé non publié ; séances listées sur <https://www.college-de-france.fr/fr/agenda/cours/les-migrations-la-lumiere-du-droit> (28/10/2022-4/1/2023) | Non relevé (contenu absent). | D |
| 2023-24, *Colonisation et migration* | 🔎 idem ; <https://college-de-france.fr/fr/agenda/cours/colonisation-et-migration> (27/10/2023-12/1/2024) | Non relevé. | B |
| 2024-25, *Religions et migrations* | 🔎 idem ; ✅ programme des 8 cours : <https://www.college-de-france.fr/fr/agenda/cours/religions-et-migrations> (8/11/2024-17/1/2025) | Titres seuls : « creuset français », laïcité, droits des femmes, héritage chrétien. | hors périmètre |
| Leçon de clôture, 15/5/2025 | ✅ *Face à l'immigration, le savant et le politique*, Collège de France, coll. « Leçons de clôture », 16/4/2026, 152 p. | Contient « Une progression continue depuis 2000, mais moins rapide pour la France » (p. 63-65, d'après GC note 5). | G |

**Le cours du 6/11/2020 (✅ Annuaire 2020-21, p. 600-601).** Intitulé « Visions complotistes : la singulière histoire des "migrations de remplacement" ». Origine de la thèse : le rapport de la Division de la population de l'ONU, *Migrations de remplacement*, **mars 2000**. Six scénarios de projection ; le dernier (geler le rapport entre générations par la seule immigration) exige des effectifs « astronomiques et totalement irréalistes » : un **scénario contrefactuel, de « démographie-fiction »**. Seuls sont réalistes ceux qui stabilisent la population d'âge actif ou la population totale. Conclusion : le vieillissement « ne peut être aboli » (« par le bas » : fécondité ; « par le haut » : longévité). Document inédit : récit de la genèse recueilli auprès de Joseph-Alfred Grinblat. Contresens successifs de la presse puis de l'extrême droite. Précédent : le plan d'**Alfred Sauvy** (1945-46, 5 millions de migrants pour combler les « creux » de la pyramide), obsolète dès 1946 avec le baby-boom. Réflexion finale : les démographes sous-estiment l'effet de leurs exercices de substitution dans le débat public. Opposition de la vision « gravitaire » à la vision « complotiste ». Prolongement écrit : F. Héran, « Science et complot : l'étrange fortune du rapport de l'ONU sur les "migrations de remplacement" (2000-2020) », in J. Baechler et G. Bronner (dir.), *L'Irrationnel aujourd'hui*, Hermann, 2021, p. 265-302 (✅ référence ; texte 🔎 non lu). Rappel déclaré : citation de M. Le Pen, sept. 2015 (« submersion migratoire » « sciemment » orchestrée par l'UE et l'ONU).

### Gestes à ajouter ou à préciser (H15 et suivants)

| # | Geste | Source | Traduction sur le site |
|---|---|---|---|
| H15 | **Scénario contrefactuel explicite.** Les « migrations de remplacement » sont un exercice de démographie-fiction qui montre l'impossible, non un plan. Dire de chaque projection ce qu'elle est (prévision, scénario, contrefactuel). | Annuaire 2020-21, p. 600 | F4 ; étiquette de statut sur toute projection |
| H16 | **Vieillissement « par le bas » et « par le haut ».** L'immigration ne l'abolit pas ; elle retarde la baisse de la population d'âge actif. | idem, p. 600 | F (pyramides, ratio) |
| H17 | **Méfiance envers les mégaphores.** Héran classe les métaphores aquatiques (flux, afflux, submersion, tsunami, trop-plein) parmi les « modèles naturalistes » : la métaphore « n'explique pas, elle *transplique* ». **La piscine du site est elle-même une mégaphore aquatique** : à assumer comme comptabilité (stocks et flux), pas comme explication ; contraster avec la « submersion ». | Annuaire 2021-22, p. 637-638 | A : légende et garde-fous |
| H18 | **Bestiaire des arguments** : pente glissante, « bon sens » contre statistique officielle, jugement de folie, amalgame vs dissociation (Perelman), perversité / futilité / mise en péril (Hirschman). | Annuaire 2021-22, p. 636-638 | G1 (typologie en plus des sophismes chiffrés) |
| H19 | **Multiplicateurs et équivalents-ville** : « ×25 sur l'accroissement annuel moyen », « ×60 » pour les Afghans, « l'équivalent de Lyon ». À traduire en % de la population et en niveaux. | Note OID, p. 21-24 | G1 |
| H20 | **Préférences révélées.** On ne démontre pas l'« appel d'air » en comparant la générosité des dispositifs : on regarde où les migrants sont effectivement allés (« attractivité » = attirer plus que ses voisins). | ICM 46-47 ; Note OID p. 6-8 | C ; encadré G |
| H21 | **Capacités d'accueil : structurelles vs construites.** Population et PIB sont des données ; hébergement, personnel, législation sont des décisions. | ICM 49 | G ; clarifier le terme |
| H22 | **Entonnoir désir → projet → réalisation.** Gallup : 14 % veulent partir, 1,5 % prévoient de le faire dans l'année, 0,5 % préparent leur départ. | Annuaire 2017-18, p. 532 | G2, F (prophéties) |
| H23 | **Diasporas et chaînes migratoires** comme déterminant du choix de destination (Ukrainiens : diasporas existantes plus que l'allocation). | ICM 41 ; Annuaire 2018-19 (cours 4) | C |
| H24 | **Précisions sur H8** : stagnation 1975-1999 autour de 7,3 %, puis hausse continue depuis 2000 (11,3 % en 2024) ; ce n'est donc pas « une courbe qui monte depuis toujours ». **Sur H3** : la définition internationale de l'immigré vient de la Division de la population de l'ONU, non du HCI ; les nationaux nés à l'étranger de parents expatriés sont exclus. **Sur H12** : ajouter « dilution » à « infusion » (GC p. 8 : 41 % de liens sur trois générations, < 6 % avec quatre grands-parents immigrés). | Note OID p. 23 ; Annuaire 2017-18 p. 530 ; GC | B1, C, E |
| H25 | **Solde migratoire = mouvements d'immigrés + mouvements de non-immigrés** (sorties de natifs comprises) ; relève de l'équation fondamentale. | GC p. 3 | A, D5 |

---

## 4. La « piscine », les formules d'accroche

**Piscine / baignoire : 🔎 non trouvée.** Aucune occurrence de « piscine », « baignoire » ou « bassin » dans : ICM, AFD, extrait des 30Q, cinq résumés de l'Annuaire, GC, Note OID (recherche par script sur les `.txt`). Recherches web (Héran, Le Bras, Tribalat, « baignoire », « bonde », « renouvellement des générations ») : aucun résultat pertinent. Images voisines, **toutes aquatiques mais utilisées pour les critiquer** :
- « vases communicants » et « trop-plein qui déborde » (Annuaire 2017-18, p. 528) ;
- « métaphores aquatiques : écoulement du trop-plein (flux, afflux, submersion, tsunami) » et analyses de Marc Bernardot (2016) (Annuaire 2021-22, p. 638) ;
- Héran définit l'immigré par la formule « résultante des entrées, des sorties et des décès » (ICM 6, AFD 10), c'est-à-dire un bilan de stock qui est la baignoire sans le nom.

La métaphore de la baignoire ou de la piscine reste donc, à ce stade, **une proposition propre au site**. 🔎 À ne pas attribuer à Héran ; l'étayer par les formules ci-dessous.

| Formule | Source exacte | Statut |
|---|---|---|
| « infusion durable et non d'une intrusion massive » | Annuaire 2017-18, p. 528 ✅ (leçon inaugurale 5/4/2018) ; repris dans GC p. 8 (« invasion » vs « infusion durable allant de pair avec une dilution ») ✅ | ✅ |
| « grand renouvellement » (« notre horizon n'est pas le "grand remplacement", mais plutôt le "grand renouvellement" ») | Note de lecture de *Immigration : le grand déni* (Seuil, 2023) sur <https://www.melchior.fr/sites/melchior/files/fichiers/Livre%20HERAN.pdf>, p. 1 : **pas de texte d'Héran lu** | 🔎 formule rapportée par un tiers ; vérifier dans le livre |
| « On peut la réguler mais pas l'inverser » | ICM, diapo 15 ✅ (« Tendance lourde, de niveau mondial… elle n'est pas réversible à volonté ») | ✅ |
| « Tout le contraire du "grand remplacement" » | ICM, diapo 14 ✅ | ✅ |
| « Qui détient la clef pour stopper, voire inverser, ce mouvement mondial ? » | AFD, diapo 19 ✅ | ✅ |
| « Deux vérités » (la migration progresse en Europe et dans le monde ; en France à un rythme moindre) | AFD, diapo 16 ✅ | ✅ |
| « Linéaire, nullement exponentielle » ; « prétendre que l'immigration explose est une contrevérité » | ICM, diapo 15 ✅ ; AFD 19 ✅ | ✅ |
| « Il faut faire avec, parce qu'on peut difficilement faire sans » | GC p. 7 ✅ | ✅ |
| « Pas un complot, mais pire qu'un complot » (le grand récit migratoire) | Annuaire 2021-22, p. 637 ✅ | ✅ (c'est une description de l'adversaire) |
| « Nous devrons vivre avec le vieillissement » | Annuaire 2020-21, p. 600 ✅ | ✅ |
| « Pas la misère du monde mais la richesse émergente » | Annuaire 2017-18, p. 528 ✅ | ✅ |
| « un droit au non-remplacement » (désigne la chimère d'un entre-soi) | GC p. 7 ✅ | ✅ |

---

## 5. Contradicteurs et polémique de 2026

| Pièce | État | Référence |
|---|---|---|
| Tribune du *Monde*, 11 mai 2026 | ✅ existe. **C'est une tribune collective de l'Institut Convergences Migrations** (signataires : M.-C. Saglio-Yatzimirsky, F. Gubert, A. Pécoud, H. Thiollet, H. Rapoport, P. Simon, F. Héran…), pas une tribune signée d'Héran seul. Texte *Le Monde* 🔎 (accès payant), lu via la republication ICM. | Titre ICM : « La science n'est pas une opinion. Réponse aux attaques contre la recherche sur les migrations », <https://www.icmigrations.cnrs.fr/2026/05/12/la-science-nest-pas-une-opinion-reponse-aux-attaques-contre-la-recherche-sur-les-migrations-tribune-de-licm/> ; titre *Le Monde* d'après Wikipédia : « Sous le couvert de l'objectivité, l'Observatoire de l'immigration et de la démographie pratique une sélection biaisée des données pour nourrir un discours alarmiste » (URL Wikipédia, non ouverte) |
| Note longue d'Héran, 12 mai 2026 (37 p.) | ✅ | `gc/note_heran_oid.pdf` ; <https://www.icmigrations.cnrs.fr/wp-content/uploads/2026/05/OID_Analyse-FH_11-05-2026_logoICM.pdf> |
| Fact-check AFP, juin 2026 | 🔎 **texte introuvable** (non indexé). Seules traces : le *Figaro* (extrait repris par Fondapol) évoque un fact-check AFP du **5 juin** sur des « chiffres brandis sur le thème de l'immigration » et résume : « aucun chiffre faux, mais des interprétations qui ne conviennent pas aux chercheurs de Convergences Migrations » ; Breizh-info (10/6/2026, source militante) affirme qu'« à défaut de chiffres faux » l'AFP s'est rabattue sur les graphiques, **un seul grief cité : l'axe vertical tronqué** | <https://www.fondapol.org/dans-les-medias/immigration-depuis-trente-ans-le-grand-virage-a-gauche-de-lined-et-la-mise-au-pas-des-enfants-dalfred-sauvy/> ; <https://www.breizh-info.com/2026/06/10/261058/ined-comment-la-demographie-francaise-a-ete-colonisee-par-lideologie-migratoire/> |
| Article du *Figaro*, 9 juin 2026 | ✅ Alexis Feertchak, « Immigration : depuis 30 ans, le grand virage à gauche de l'Ined et la mise au pas des enfants d'Alfred Sauvy ». Texte intégral 🔎 (payant) ; contenu connu par la réponse d'Héran (GC p. 1-3) et l'extrait Fondapol. Le *Figaro* ne porte pas sur les graphiques mais sur la gestion de l'Ined par Héran (1999-2009) | URL dans GC, note 1 (slug daté 20260608) |
| Réponse d'Héran, *La Grande Conversation*, 2 juillet 2026 | ✅ 25 p., 16 points | <https://www.lagrandeconversation.com/app/uploads/2026/07/lined-et-la-demographie-en-peril-ou-le-mythe-du-fossoyeur-la-grande-conversation.pdf> |

**Choix graphiques reprochés à l'OID (côté Héran et ICM).** ✅ Note OID : chiffres absolus au lieu de proportions (p. 21-23) ; chiffre absolu comparé à une ville (« l'équivalent de Lyon », Retailleau, janv. 2025) ; « multiplicateurs » (accroissement annuel moyen 2023-24 « ×25 » vs 1990-99, « ×60 » pour les Afghans, police de caractères surdimensionnée, p. 23-24) ; sélection dans les tableaux de l'OCDE (p. 17-19) ; abus de la rhétorique de la « ruée ». Tribune ICM : classement « 2e pays de l'UE le plus attractif » fondé sur les demandes d'asile en absolu, alors qu'en rapportant à la population la France serait 12e sur 2014-2024. ✅ Une carte de l'OID dans le *JDD* est critiquée par un blog (C. Lhomme, 9/2/2026) pour une **légende à pas irréguliers (2,5 %, puis 5 %, puis 20 %)** : source unique, pas l'AFP. Antécédent : cartes de France Stratégie utilisées par l'OID en 2021 (*Le Monde*/Décodeurs, 23/2/2022, d'après Wikipédia, 🔎 non ouvert).

**Choix défendus par Héran.** Taux par habitant, périodes longues (dix ans) pour ne pas se laisser piéger par 2015 ou le Covid, hypothèse maximaliste sur les déboutés (ICM 26), courbe Insee « directe » plutôt que multiplicateurs, bascule absolu/relatif en deux diapos.

**Points de vigilance pour le site.** (1) L'axe tronqué n'est pas un tabou chez les uns (selon Breizh-info, courant dans l'Insee) : le site doit **commencer à zéro ou le signaler**. (2) Les graphiques d'Héran ne sont pas exempts : axe tronqué à 170 en ICM 25, double axe en ICM 7, échelles différentes par panneau en ICM 17, indice base 2000 qui masque les niveaux en AFD 18, anomalie des chiffres en ICM 32. (3) Le plaidoyer « par habitant » a sa limite assumée par l'adversaire : « 100 000 Afghans en douze ans, c'est massif » (GC p. 15). Montrer les deux échelles plutôt qu'imposer l'une.

**Version forte de l'adversaire (OID, <https://observatoire-immigration.fr/etudes-et-notes/>).** Liste des notes lue sur le site (🔎 contenus lus via un résumé automatique, à relire). Les plus pertinentes :
- **« Les scénarios démographiques de la France au XXIe siècle » (21 sept. 2026)** : projection à 2100 par origine sur trois générations (« sans ascendance migratoire », européenne, extra-européenne), 3 scénarios d'entrées (350 000 / 250 000 / restrictif) ; les « sans ascendance migratoire » deviendraient minoritaires vers 2050 (haut), 2060 (intermédiaire) ; pas d'émigration modélisée, y compris des natifs ; fécondité des natives uniforme. <https://observatoire-immigration.fr/les-scenarios-demographiques-de-la-france-au-xxie-siecle/>. **C'est la « version forte » du « remplacement »** que le curseur de définition (F2) et la piscine devront affronter, et elle est postérieure à la polémique.
- « Bilan migratoire de la présidence Macron » (25/1/2024) ; « L'immigration aujourd'hui : flux (8/3/2023) et stocks (10/3/2023) » ; « L'immigration dans les territoires : quinze ans de bouleversement » (26/9/2024, cartes communales) ; « Enrayer la chute de la natalité » (12/10/2026) ; « L'immigration afghane en France : un événement de grande ampleur » (4/6/2025) ; « L'asile… 580 millions de bénéficiaires potentiels » (17/1/2025).
- Livre : N. Pouvreau-Monti, *Immigration, mythes et réalités*, Fayard, avril-mai 2026 (date : 15 avril 2026 selon GC p. 15).

---

## 6. Le corpus des 206 publications « n idées reçues »

🔎 **Pas de corpus public trouvé.** ✅ Ce qui est public : le résumé statistique (AFD, diapos 4 et 5 : types d'émetteurs, courbe annuelle, les 30 idées les plus fréquentes avec leurs fréquences). La diapo 4 renvoie à un « article pour *Maux d'exil*, la revue du Comede » : ✅ F. Héran, « Immigration : comment lutter contre les idées reçues ? », *Maux d'exil* n° 83, déc. 2025 (sommaire sur <https://www.comede.org/maux-dexil-pour-en-finir-avec-les-idees-fausses-sur-les-migrations/>, pages 2-3 d'après une recherche web non recoupée) ; pas de PDF isolé ni de liste des 206 titres trouvés. Pistes non ouvertes (accès 403 ou non tentées) : *Hermès* 2024/2 p. 101 (« François Héran : recenser les idées reçues sur la migration », Cairn) ; *Migrations Société* 2026/1 p. 117 (« Recherche scientifique contre sens commun ? », Cairn). **À demander à Héran ou à l'ICM** si la liste existe sous forme de tableur.

---

## 7. Écarts avec le cadrage

1. **« Tribune d'Héran dans *Le Monde* »** : c'est une tribune collective de l'ICM (Héran parmi les signataires), du 11 mai 2026. Le texte à son seul nom est la note de 37 p. du 12 mai sur le site de l'ICM.
2. **Fact-check AFP « sur les représentations graphiques »** : non vérifié. Les sources neutres retrouvées parlent de « chiffres » ; seule une source militante mentionne les graphiques (axe tronqué). Le texte AFP reste à localiser avant d'affirmer quoi que ce soit.
3. **Le *Figaro* du 9 juin** ne porte pas sur les graphiques mais sur l'Ined et la gestion d'Héran ; l'OID n'y est qu'un angle (selon Héran, « la véritable raison de son article »).
4. **« 30 questions »** : le sommaire de l'édition 2021 compte **33 entrées**. De plus, une **4e édition refondue, intitulée *L'Immigration en 30 questions*** (La Documentation française, « Doc en poche », avril 2026), existe (GC, note 2) : le plan à utiliser est peut-être celui-là, 🔎 sommaire non vu.
5. **Cycles du Collège de France** : les intitulés cités sont corrects, mais **seuls cinq résumés existent** (2017-18 à 2021-22). Ceux de 2018-19 et 2019-20 ne sont que des listes d'intitulés ; ils n'apportent ni angles ni graphiques. L'« extraction des graphiques mobilisés » n'est possible que pour 2017-18, 2020-21 (partiellement) et 2021-22.
6. **Leçon de clôture** : prononcée le 15 mai 2025, **publiée le 16 avril 2026** (152 p.) ; une version « refondue » existe, donc le texte diffère de la leçon orale.
7. **« Piscine »** : le cadrage la présente comme une métaphore à trouver chez Héran ; introuvable. Héran critique justement les métaphores aquatiques (cours du 3/12/2021).
8. **Définition de l'immigré** : la distinction étranger/immigré a été annoncée par l'Insee et l'Ined en 1991, mais la définition internationale (né à l'étranger, installé ≥ 1 an) est celle de la Division de la population de l'ONU, pas du HCI (Annuaire 2017-18, p. 530). La progression de la France depuis 2000 est « +59 % » dans ICM 10 (ONU 2020) et « +50 % » dans AFD 18 (ONU 2024, France hexagonale) : ne pas mélanger les éditions.
9. **« 5 % des petits-enfants » (ICM 14) et « < 6 % » (GC p. 8)** : deux chiffres pour la même statistique ; à trancher sur TeO2.
10. **Graphique ICM 32** : données apparemment copiées de la diapo 30 (voir §1.1).
11. **OID, nom** : « Observatoire de l'immigration et de la **démographie** » (GC p. 3 écrit une fois « de l'intégration »).

---

## 8. Recommandations pour la v1 (synthèse)

- **À reprendre tel quel** : AFD 10 (part d'immigrés par pays, France 17e), AFD 25-29 (entrées par catégorie pour 10 000 hab.), ICM 30 (paire absolu → relatif) et ICM 40 (part des réfugiés ukrainiens vs part du PIB), AFD 14-15 (taux d'émigrés).
- **À mettre à jour** : ICM 7-8 (série 1851-2025), AFD 18 (+50 % ; vérifier avec l'édition ONU la plus récente), ICM 17 / AFD 23 (titres jusqu'à 2025), ICM 24-28 (asile jusqu'à 2025).
- **À améliorer** : spaghetti d'ICM 24-25 ; double axe d'ICM 7 ; échelles par panneau d'ICM 17.
- **Manque dans le corpus d'Héran** : aucun graphique dynamique de la piscine, ni de projections par origine. La version forte de l'adversaire en 2026 (note OID de septembre) en propose une ; le site devra y répondre point par point (émigration des natifs, convergence de fécondité, mixité).
