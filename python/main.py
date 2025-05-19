from ursina import *
import pyautogui
app = Ursina()
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
camera.position = (0, 30, 0)  # En hauteur, reculée
camera.rotation_x = 90          # Orientation vers le bas
pon = Entity(
    model='cube',
    color=color.orange,
    position=(-4, 1.5, -4),  # Position initiale
    scale=(1, 2, 1)  # Échelle sur l'axe Y pour faire un "pion"
)
enemypon = Entity(
    model='cube',
    color=color.blue,
    position=(3, 1.5, 3),  # Position initiale
    scale=(1, 2, 1)  # Échelle sur l'axe Y pour faire un "pion"
)

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
def on_pon_clicked():
    pon.color = color.red
    print("Pion cliqué !")
def update():
    
    if pon.position == enemypon.position:
        enemypon.scale = (0.5, 0.5, 0.5)

for x in range(taille):
    for z in range(taille):
        color_case = color.white if (x + z) % 2 == 0 else color.black
        Entity(
            model='cube',
            color=color_case,
            position=(x - offset, 0, z - offset),  # On décale pour centrer
            scale=1
        )


app.run()
