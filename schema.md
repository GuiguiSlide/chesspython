# Règles des Échecs

## Objectif du jeu
Le but est de mettre le roi adverse en échec et mat, c’est-à-dire de le menacer de capture sans qu’il puisse s’échapper.

## Plateau
- 64 cases (8x8), alternant clair et foncé:
    faire un tableau(aspect graphique)
- Chaque joueur commence avec 16 pièces : 1 roi, 1 dame, 2 tours, 2 fous, 2 cavaliers, 8 pions.
    faire des pions placés sur le tableau(graphique et )

## Déplacement des pièces
- **Roi** : une case dans toutes les directions.
- **Dame** : autant de cases que souhaité, dans toutes les directions.
- **Tour** : autant de cases que souhaité, horizontalement ou verticalement.
- **Fou** : autant de cases que souhaité, en diagonale.
- **Cavalier** : en “L” (deux cases dans une direction, puis une perpendiculaire).
- **Pion** : avance d’une case, capture en diagonale, peut avancer de deux cases au premier coup.

## Règles spéciales
- **Roque** : mouvement spécial du roi et d’une tour.
- **Prise en passant** : capture spéciale des pions.
- **Promotion** : un pion atteint la dernière rangée est promu (souvent en dame).

## Fin de la partie
- **Échec et mat** : le roi est menacé et ne peut s’échapper.
- **Pat** : le joueur n’a plus de coup légal, mais n’est pas en échec (égalité).
- **Nulle** : plusieurs situations mènent à l’égalité (matériel insuffisant, répétition, etc.).
TODO:
tester par rapport a toutes les cases vides 
fait que pour arriver la il faut que la prochaine case soit libre
dès que case occuper peut pas aller plus loins
tant que case libre mouvement possible
utiliser while