import copy
import random
from ursina import *

app = Ursina()
window.borderless = False
window.fullscreen = True
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
camera.position = (0, 30, 0)  # En hauteur, reculée
camera.rotation_x = 90          # Orientation vers le bas
ponarmy = []
enemyponarmy = []

class Move(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
            print(f"Tu as cliqué sur : {self.name}")
            self.visible = False

            possiblemoves.visible = False
            possiblemoves2.visible = False
            possiblemoves3.visible = False
            possiblemoves4.visible = False
            possiblemoves5.visible = False
            possiblemoves6.visible = False
            possiblemoves7.visible = False
            possiblemoves8.visible = False
            
            if knight1.color == color.red:
                knight1.position = (self.position.x, self.position.y, self.position.z)  # Déplace le cavalier
                knight1.color = color.yellow  # Change la couleur pour feedback

            if knight2.color == color.red:
                knight2.position = (self.position.x, self.position.y, self.position.z)
                knight2.color = color.yellow  # Change la couleur pour feedback   

            for pon in ponarmy:
                if pon.color == color.red:
                    pon.position = (self.position.x, self.position.y, self.position.z)  # Déplace le pion
                    pon.color = color.orange  # Change la couleur pour feedback
            
            if king.color == color.red:
                king.position = (self.position.x, self.position.y, self.position.z)
                king.color = color.gray
    def update(self):
        if self.position == pon.position :
            self.position = (1000,1000,1000)
        if self.position == knight1.position :
            self.position = (1000,1000,1000)
        if self.position == knight2.position :
            self.position = (1000,1000,1000)
        if self.position == king.position :
            self.position = (1000,1000,1000)

class Pion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    
    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        possiblemoves.visible = False
        possiblemoves2.visible = False
        possiblemoves3.visible = False
        possiblemoves4.visible = False
        possiblemoves5.visible = False
        possiblemoves6.visible = False
        possiblemoves7.visible = False
        possiblemoves8.visible = False
        if self.color == color.orange:
            for pon in ponarmy:
                pon.color = color.orange
            knight1.color = color.yellow
            knight2.color = color.yellow
            king.color = color.gray
            self.color = color.red  # Change la couleur pour feedback 
# Check capture on forward-left diagonal (x - 1, z + 1)
            if (self.position.x, self.position.y, self.position.z) == (enemypon.position.x - 1, enemypon.position.y, enemypon.position.z + 1):
                possiblemoves.color = color.green
                possiblemoves.position = (enemypon.position.x - 1, enemypon.position.y, enemypon.position.z + 1)
                possiblemoves.visible = True

            # Check capture on forward-right diagonal (x + 1, z + 1)
            if (self.position.x, self.position.y, self.position.z) == (enemypon.position.x + 1, enemypon.position.y, enemypon.position.z + 1):
                possiblemoves2.color = color.green
                possiblemoves2.position = (enemypon.position.x + 1, enemypon.position.y, enemypon.position.z + 1)
                possiblemoves2.visible = True

            # Check normal forward move (x, z + 1)
            # Assuming no enemy is on the forward square
            if (self.position.x, self.position.y, self.position.z + 1) != (enemypon.position.x, enemypon.position.y, enemypon.position.z):
                possiblemoves3.color = color.green
                possiblemoves3.position = (self.position.x, self.position.y, self.position.z + 1)
                possiblemoves3.visible = True
            else:
                # If enemy is blocking forward move, maybe you want to do nothing or handle differently
                pass

        else:
            self.color = color.orange  # Change la couleur pour feedback
            possiblemoves.visible = False
            possiblemoves2.visible = False
            possiblemoves3.visible = False

class King(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        if self.color == color.gray:
            for pon in ponarmy:
                pon.color = color.orange
            knight1.color = color.yellow
            knight2.color = color.yellow
            self.color = color.red
            possiblemoves.color = color.green
            possiblemoves2.color = color.green
            possiblemoves3.color = color.green
            possiblemoves4.color = color.green
            possiblemoves5.color = color.green
            possiblemoves6.color = color.green
            possiblemoves7.color = color.green
            possiblemoves8.color = color.green
            possiblemoves.position = (self.position.x+1, self.position.y, self.position.z)
            possiblemoves2.position = (self.position.x-1, self.position.y, self.position.z)
            possiblemoves3.position = (self.position.x+1, self.position.y, self.position.z+1)
            possiblemoves4.position = (self.position.x-1, self.position.y, self.position.z-1)
            possiblemoves5.position = (self.position.x, self.position.y, self.position.z+1)
            possiblemoves6.position = (self.position.x-1, self.position.y, self.position.z+1)
            possiblemoves7.position = (self.position.x+1, self.position.y, self.position.z-1)
            possiblemoves8.position = (self.position.x, self.position.y, self.position.z-1)
            possiblemoves.visible = True
            possiblemoves2.visible = True
            possiblemoves3.visible = True
            possiblemoves4.visible = True
            possiblemoves5.visible = True
            possiblemoves6.visible = True
            possiblemoves7.visible = True
            possiblemoves8.visible = True
        else:
            self.color = color.gray  # Change la couleur pour feedback
            possiblemoves.visible = False
            possiblemoves2.visible = False
            possiblemoves3.visible = False
            possiblemoves4.visible = False
            possiblemoves5.visible = False
            possiblemoves6.visible = False
            possiblemoves7.visible = False
            possiblemoves8.visible = False

class Knight(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        if self.color == color.yellow:
            for pon in ponarmy:
                pon.color = color.orange
            knight1.color = color.yellow
            knight2.color = color.yellow
            king.color = color.gray
            self.color = color.red
            possiblemoves.color = color.green
            possiblemoves2.color = color.green
            possiblemoves3.color = color.green
            possiblemoves4.color = color.green
            possiblemoves5.color = color.green
            possiblemoves6.color = color.green
            possiblemoves7.color = color.green
            possiblemoves8.color = color.green
            possiblemoves.position = (self.position.x+1, self.position.y, self.position.z+2)
            possiblemoves2.position = (self.position.x-1, self.position.y, self.position.z+2)
            possiblemoves3.position = (self.position.x+1, self.position.y, self.position.z-2)
            possiblemoves4.position = (self.position.x-1, self.position.y, self.position.z-2)
            possiblemoves5.position = (self.position.x+2, self.position.y, self.position.z+1)
            possiblemoves6.position = (self.position.x-2, self.position.y, self.position.z+1)
            possiblemoves7.position = (self.position.x+2, self.position.y, self.position.z-1)
            possiblemoves8.position = (self.position.x-2, self.position.y, self.position.z-1)
            possiblemoves.visible = True
            possiblemoves2.visible = True
            possiblemoves3.visible = True
            possiblemoves4.visible = True
            possiblemoves5.visible = True
            possiblemoves6.visible = True
            possiblemoves7.visible = True
            possiblemoves8.visible = True
        else:
            self.color = color.yellow  # Change la couleur pour feedback
            possiblemoves.visible = False
            possiblemoves2.visible = False
            possiblemoves3.visible = False
            possiblemoves4.visible = False
            possiblemoves5.visible = False
            possiblemoves6.visible = False
            possiblemoves7.visible = False
            possiblemoves8.visible = False

class EnemyPion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self):
        targets = ponarmy + [knight1, knight2, king]

        for target in targets:
            if target.position == self.position and self.color == color.blue:
                self.visible = False
                self.position = (1000, 1000, 1000)
        
def input(key):
    if key == 'escape':
        exit();
    
    if key == 'f':  # fullscreen
        if not window.fullscreen:
            window.fullscreen = True
        else:
            window.fullscreen = False

    if key == 'b':# debug button
        print(pon.position)
        print(enemypon.position)
        print(possiblemoves.position)
        print(possiblemoves2.position)
        print(knight1.position)
        print(knight2.position)
        print(ponarmy)
        print(enemyponarmy)
        return

for x in range(taille):
    for z in range(taille):
        color_case = color.white if (x + z) % 2 == 0 else color.black
        Entity(
            model='cube',
            color=color_case,
            position=(x - offset, 0, z - offset),  # On décale pour centrer
            scale=1
        )
# Placement des pions et cavaliers
for x in range(taille):
    pon = Pion(
        model='cube',
        color=color.orange,
        position=(x-4, 1.5, -3),  # Ligne 2 (rangée des pions)
        scale=(1, 2, 1),
        name=f'pon{x}'
        )
    ponarmy.append(pon)

    enemypon = EnemyPion(
        model='sphere',
        color=color.blue,
        position=(x-4, 1.5, 2),  # Ligne 7 (rangée des pions adverses)
        scale=(1, -2, 1),
        name=f'enemypon{x}'
        )
    enemyponarmy.append(enemypon)
    
# Positionner les deux cavaliers (knights) aux positions classiques d'échecs
knight1 = Knight(
    model='cube',
    color=color.yellow,
    position=(-4+1, 1.5, -4),  # b1
    scale=(1, 2, 1)
    )
knight2 = Knight(
    model='cube',
    color=color.yellow,
    position=(-4+6, 1.5, -4),  # g1
    scale=(1, 2, 1)
    )
king = King(
    model='cube',
    color=color.gray,
    position=(-4+3, 1.5, -4),  # e1
    scale=(1, 2, 1)
    )
#on en as besoin de 8 pour les chevaliers #4 pour les fous #4 pour les tours #8 pour la reine #2 pour les pions #8 pour le roi
possiblemoves = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves2 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves3 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves4 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves5 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves6 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves7 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
possiblemoves8 = Move(
    model='cube',  # Position initiale
    scale=(1, 1.9, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )



app.run()
