# Conception du site v1

**Statut : proposition du 2026-11-16, à valider par Max.** Échantillon visuel :
page privée publiée pour la revue (les chiffres y sont ceux de l'export du
2026-11-16, recopiés pour l'échantillon ; sur le site, ils sont lus par script).

## 1. Le sujet, le public, la tâche

- **Sujet** : un instrument de mesure. Le site ne plaide pas, il rapporte,
  compare, dit sa précision et ses champs. La piscine en est le module
  signature : la population comme une eau qui se renouvelle.
- **Public** : non-spécialistes (enseignants, élèves, journalistes, citoyens
  qui ont entendu la thèse) ; secondairement, des lecteurs qui vérifient.
- **Tâche première** : montrer et laisser vérifier les chiffres. Tout ce qui
  ne sert pas cette tâche est retiré.

## 2. L'idée directrice : l'échelle limnimétrique

La règle émaillée graduée qui mesure le niveau d'une rivière ou d'un bassin
relie les deux registres du site : **mesurer** et **l'eau**. Ses graduations en
« E » et les **repères de crue** (plaques datées des niveaux passés, sur les
ponts et les façades) donnent le seul élément marquant du site : l'ouverture de
l'accueil montre la part des immigrés comme un niveau d'eau, de 1921 à 2025,
avec des plaques pour les niveaux passés. Ailleurs, le motif reste discret :
filets et graduations pour les axes, pas de décor.

## 3. Jetons

### Couleurs : le bleu appartient aux données

Le site lui-même est à l'encre ; **tout le bleu est de la donnée** (la rampe
des générations, l'eau). Une seule couleur de repère, ocre, marque les
niveaux, le focus clavier et les codes d'incertitude. Aucun rouge.

| Jeton | Clair | Sombre | Rôle |
|---|---|---|---|
| `--papier` | `#f6f7f5` | `#10171c` | fond (émail, blanc cassé froid) |
| `--encre` | `#15212b` | `#e7ecee` | texte, graduations, liens soulignés d'ocre |
| `--ardoise` | `#4c5a65` | `#a6b3bb` | texte secondaire |
| `--reglure` | `#ccd4d8` | `#2b363d` | filets, cadres |
| `--repere` | `#c08a12` | `#e3ad3a` | niveaux, focus, codes U (marques, pas de texte) |
| `--repere-texte` | `#865f05` | `#e8b84f` | le repère quand il porte du texte |
| `--t0` à `--t4` | inchangés | inchangés | rampe des générations (validée le 2026-11-16) |

Les liens sont à l'encre, soulignés d'ocre : ils ne se confondent pas avec les
données.

### Typographie

- **Barlow Semi Condensed** (OFL) : titres, chiffres mis en avant,
  graduations. Grotesque technique, proche des caractères de signalétique et
  d'instruments ; chiffres tabulaires.
- **Atkinson Hyperlegible Next** (OFL) : texte courant. Dessinée pour la
  lisibilité (Braille Institute) ; distingue 1, l, I et 0, O, ce qui compte
  sur un site de chiffres.
- Échelle : 0,8125 / 1,0625 / 1,3125 / 1,75 / 2,5 / 3,75 rem. Texte à gauche,
  colonne de lecture de 38 rem au plus. Polices hébergées par le site
  (paquets `@fontsource`), aucune ressource tierce.
- Remplace Lexend (provisoire depuis la v0).

## 4. Mise en page

- Colonne de lecture alignée à gauche ; les figures peuvent s'élargir à 64 rem.
- En-tête : la marque à gauche, la navigation à droite ; la page courante
  soulignée d'ocre.
- **Accueil** : titre, chapeau, concession chiffrée à gauche ; l'échelle à
  droite (dessous sur mobile) ; puis trois portes (piscine, temps long,
  générations) séparées par des filets, sans cartes.
- **Pages** : chaque section est une question (`h2`), sa réponse chiffrée
  juste dessous, puis la figure, puis « Le détail » replié (inchangé).
- **Figures** : un filet épais à l'encre au-dessus, le titre, le graphique,
  puis Lecture, Champ, Source et les codes U en plaques ocre. Graduations
  légères en fond des barres.

## 5. Principes

1. Une seule audace, l'échelle de l'accueil ; tout le reste est sobre.
2. Le bleu est réservé aux données ; l'ocre aux repères ; jamais de rouge.
3. Pas de cartes, pas d'ombres : des filets, comme sur une règle.
4. Chiffres en Barlow, tabulaires, toujours avec leur unité et leur champ.
5. Clair et sombre soignés tous les deux ; focus clavier visible (ocre) ;
   mouvement réduit respecté (l'eau ne monte pas si l'utilisateur l'a refusé).

## 6. Suite

Après validation : polices auto-hébergées, jetons dans `site/src/app.css`,
accueil avec l'échelle lue dans `data/export/` (parts des recensements, plaques
choisies par règle : premier point, sommet d'avant-guerre, sommet des Trente
Glorieuses, dernier point), puis gabarits des pages et des figures.
