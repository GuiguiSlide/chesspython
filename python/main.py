from ursina import *
import copy
import random
app = Ursina()
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
camera.position = (0, 30, 0)  # En hauteur, reculée
camera.rotation_x = 90          # Orientation vers le bas

class Pion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        if self.color == color.orange:
            self.color = color.red  # Change la couleur pour feedback 
            possiblemoves.color = color.green  # Change la couleur pour feedback
            possiblemoves.position = (self.position.x, self.position.y, self.position.z+1)  # Déplace le pion
        else:
            self.color = color.orange  # Change la couleur pour feedback


class Move(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
            print(f"Tu as cliqué sur : {self.name}")
            pon.position = (self.position.x, self.position.y, self.position.z)  # Déplace le pion
            pon.color = color.orange  # Change la couleur pour feedback

def input(key):
    if key == 'f':
        window.fullscreen = not window.fullscreen  # Toggle plein écran
        return

    if key == 'up arrow':
        pon.z += 1  # Déplacement du pion vers le haut
        enemypon.z -= 1
        return
    
    if key == 'down arrow':
        pon.z -= 1  # Déplacement du pion vers le haut
        enemypon.z += 1  # Déplacement du pion vers le haut
        return
    
    if key == 'left arrow':
        pon.x += 1  # Déplacement du pion vers le haut
        enemypon.x -= 1  # Déplacement du pion vers le haut
        return
    
    if key == 'right arrow':
        pon.x -= 1  # Déplacement du pion vers le haut  
        enemypon.x += 1
        return
    
    if key == 'b':# debug button
        print(pon.position)
        print(enemypon.position)
        return

def update():
    if pon.position == enemypon.position:
        enemypon.position =(100,100,100)

for x in range(taille):
    for z in range(taille):
        color_case = color.white if (x + z) % 2 == 0 else color.black
        Entity(
            model='cube',
            color=color_case,
            position=(x - offset, 0, z - offset),  # On décale pour centrer
            scale=1
        )
for x in range(taille):
    pon = Pion(
    model='cube',
    color=color.orange,
    position=(x-4, 1.5, -3),  # Position initiale
    scale=(1, 2, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )

    enemypon = Entity(
    model='cube',
    color=color.blue,
    position=(x-4, 1.5, 2),  # Position initiale
    scale=(1, 2, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )
    
    possiblemoves = Move(
    model='cube', # Position initiale
    scale=(1, -2, 1)  # Échelle sur l'axe Y pour faire un "pion"
    )

app.run()
