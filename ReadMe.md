# Projet Échecs Python

Ce projet est un jeu d'échecs interactif en 3D développé en Python avec le moteur graphique Ursina.

---

## Prérequis

- **Python** 3.13.3 (ou version compatible)
- **Librairie requise** : `ursina`
- (Facultatif) Pour la compilation en exécutable : `cx_Freeze`

---

## Installation

1. **Clonez ce dépôt :**
    ```bash
    git clone https://github.com/GuiguiSlide/chesspython.git
    ```
2. **Installez la librairie requise :**
    ```bash
    pip install ursina
    ```
3. (Facultatif) Pour générer un exécutable Windows :
    ```bash
    pip install cx_Freeze
    ```

---

## Lancement du jeu

Un menu principal permet désormais de choisir le mode de jeu directement.  
Pour lancer le jeu, exécutez simplement :

```bash
python menu.py
```

Vous pourrez alors sélectionner le mode multijoueur local ou joueur contre IA depuis le menu.

---

## Contenu du jeu

- Plateau d'échecs interactif en 3D (graphismes réalisés sous Blender)
- Mode joueur contre joueur local (multijoueur sur le même PC)
- Mode joueur contre IA (intelligence artificielle personnalisée)
- Interface utilisateur simple et intuitive
- Détection automatique des mouvements légaux, échecs et promotions
- Affichage des coups possibles pour chaque pièce
- Sons d'ambiance et effets sonores (déplacement, capture, victoire/défaite)
- Caméra orbitale contrôlable (touches fléchées et touche O)
- Plein écran (touche F)
- Affichage console du plateau pour debug
- Système de raccourcis clavier pour le contrôle rapide
- Code organisé en modules/classes pour chaque type de pièce et IA

---

## Structure du projet

```
projet echec python/
│
├── chessVSai/
│   ├── main.py
│   ├── setup.py
│   ├── classes/
│   └── assets/
│
├── chessVSmultiplayer/
│   ├── main.py
│   ├── setup.py
│   └── assets/
│
├── menu.py
├── ReadMe.md
└── ...
```

- **menu.py** : Menu principal pour choisir le mode de jeu
- **chessVSai/** : Mode joueur contre IA (avec intelligence artificielle)
- **chessVSmultiplayer/** : Mode joueur contre joueur local
- **assets/** : Modèles 3D, textures, musiques et sons

---

## Commandes utiles

- **O** : Activer/désactiver l'orbite de la caméra
- **Flèches gauche/droite** : Modifier la vitesse d'orbite de la caméra
- **F** : Basculer en plein écran
- **ESC** : Quitter le jeu
- **F5** : Redémarrer la partie (mode IA)
- **B** : Afficher la grille du plateau dans la console (debug)
- **Souris** : Sélectionner et déplacer les pièces

---

## Compilation en exécutable (facultatif)

Pour générer un exécutable Windows :
1. Placez-vous dans le dossier voulu (`chessVSai` ou `chessVSmultiplayer`)
2. Exécutez :
    ```bash
    python setup.py build
    ```
3. L'exécutable sera disponible dans `build/exe.win-amd64-3.13/`

---

## Limitations connues

- L'IA ne gère pas encore toutes les règles avancées (roque, prise en passant, etc.)
- Le mode multijoueur est local uniquement (pas de réseau)
- Certains bugs d'affichage ou de capture peuvent subsister selon la version d'Ursina

---

## Auteur

- Guillaume Beaufort

---

## Remerciements

- [Ursina Engine](https://www.ursinaengine.org/)
- [Blender](https://www.blender.org/) pour la création des modèles 3D

---

## Licence

Ce projet est open-source, voir le fichier LICENSE pour plus de détails.
