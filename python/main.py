#importer les bibliothèques nécessaires
from copy import deepcopy
from ursina import *
from ursina import color
#comment on lance l'application
app = Ursina()
#configurer la fenetre
window.borderless = False
window.fullscreen = True
#taille pour le damier
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
# Position de la caméra
camera.position = (0, 30, 0)  # En hauteur, reculée
camera.rotation_x = 90          # Orientation vers le bas
# liste pour stocker les pions alliés
ponarmy = []
# Liste pour stocker les pions ennemis
enemyponarmy = []
# Liste pour stocker les mouvements possibles
line_points = []
# mets le tour au joueur
turn = 0
#classe pour les mouvements
class Move(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
        print(f"Tu as cliqué sur : {self.name, self.position}")

        # Cache TOUS les moves verts présents dans line_points
        for pm in line_points:
            pm.visible = False
        line_points.clear()
        

        # Cache les 8 moves fixes si tu en as besoin
        hide_moves()

        # Cache aussi self (optionnel car self est dans line_points normalement)
        self.visible = False

        # Déplace les pièces selon leur couleur rouge
        if knight1.color == color.red:
            knight1.position = (self.position.x, self.position.y, self.position.z)
            knight1.color = color.yellow

        if knight2.color == color.red:
            knight2.position = (self.position.x, self.position.y, self.position.z)
            knight2.color = color.yellow
        
        if tower1.color == color.red:
            tower1.position = (self.position.x, self.position.y, self.position.z)
            tower1.color = color.cyan

        if tower2.color == color.red:
            tower2.position = (self.position.x, self.position.y, self.position.z)
            tower2.color = color.cyan
        
        if bishop1.color == color.red:
            bishop1.position = (self.position.x, self.position.y, self.position.z)
            bishop1.color = color.azure

        if bishop2.color == color.red:
            bishop2.position = (self.position.x, self.position.y, self.position.z)
            bishop2.color = color.azure

        for pon in ponarmy:
            if pon.color == color.red:
                pon.position = (self.position.x, self.position.y, self.position.z)
                pon.color = color.orange

        if king.color == color.red:
            king.position = (self.position.x, self.position.y, self.position.z)
            king.color = color.gray

        if queen.color == color.red:
            queen.position = (self.position.x, self.position.y, self.position.z)
            queen.color = color.pink
            
    def update(self):
        # Vérifie si la position du mouvement est égale à mon pion
        if self.position == pon.position :
            self.position = (1000,1000,1000)
        if self.position == knight1.position :
            self.position = (1000,1000,1000)
        if self.position == knight2.position :
            self.position = (1000,1000,1000)
        if self.position == king.position :
            self.position = (1000,1000,1000)
        if self.position == queen.position :
            self.position = (1000,1000,1000)
        if self.position == bishop1.position :
            self.position = (1000,1000,1000)
        if self.position == bishop2.position :
            self.position = (1000,1000,1000)
        if self.position == tower1.position :
            self.position = (1000,1000,1000)
        if self.position == tower2.position :
            self.position = (1000,1000,1000)
         #empecher la piece de sortir du damier
        if Vec3(self.position.x, self.position.y, self.position.z) <= Vec3(-5, 1.5, self.position.z):
            self.position = (1000,1000,1000)
        if Vec3(self.position.x, self.position.y, self.position.z) >= Vec3(4, 1.5, self.position.z):
            self.position = (1000,1000,1000)
        if Vec3(self.position.x, self.position.y, self.position.z) <= Vec3(self.position.x, 1.5, -5):
            self.position = (1000,1000,1000)
        if Vec3(self.position.x, self.position.y, self.position.z) >= Vec3(self.position.x, 1.5, 4):
            self.position = (1000,1000,1000)
#classe pour le pion
class Pion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        # Masquer toutes les cases de déplacement possibles
        hide_moves()
        #reinitialisation
        if self.color == color.orange:
            reset()
            self.color = color.red  

            # Position actuelle du pion
            x, y, z = self.position
            
            # 1) Vérifier capture sur diagonale avant-gauche (x-1, y, z+1)
            pos_diag_left = (x - 1, y, z + 1)
            if enemy_at_position(pos_diag_left):
                possiblemoves.color = color.green
                possiblemoves.position = pos_diag_left
                possiblemoves.visible = True
            
            # 2) Vérifier capture sur diagonale avant-droite (x+1, y, z+1)
            pos_diag_right = (x + 1, y, z + 1)
            if enemy_at_position(pos_diag_right):
                possiblemoves2.color = color.green
                possiblemoves2.position = pos_diag_right
                possiblemoves2.visible = True

            # 3) Vérifier déplacement normal vers l'avant (x, y, z+1) sans ennemi
            pos_forward = (x, y, z + 1)
            if not enemy_at_position(pos_forward) and not any(pon.position == pos_forward for pon in ponarmy):
                possiblemoves3.color = color.green
                possiblemoves3.position = pos_forward
                possiblemoves3.visible = True

        else:
            # Si on clique sur un pion rouge (sélectionné), on le désélectionne
            self.color = color.orange  
            possiblemoves.visible = False
            possiblemoves2.visible = False
            possiblemoves3.visible = False
#classe pour la reine  
class Queen(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        hide_moves()
        if self.color != color.red:
            # La reine n'est pas rouge -> on la passe en rouge
            reset()
            self.color = color.red  

            for i in range(-7, 8):
                pm1 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                pm2 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                pm3 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                pm4 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm5 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm6 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)
                pm7 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm8 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)

                line_points.extend([pm1, pm2, pm3, pm4, pm5, pm6, pm7, pm8])

        else:
            # La reine est rouge -> on la remet rose et on cache les moves
            self.color = color.pink
            for pm in line_points:
                pm.visible = False
            line_points.clear()
# classe pour le roi
class King(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        if self.color == color.gray:
            reset()
            self.color = color.red  
            color_moves()
            possiblemoves.position = (self.position.x+1, self.position.y, self.position.z)
            possiblemoves2.position = (self.position.x-1, self.position.y, self.position.z)
            possiblemoves3.position = (self.position.x+1, self.position.y, self.position.z+1)
            possiblemoves4.position = (self.position.x-1, self.position.y, self.position.z-1)
            possiblemoves5.position = (self.position.x, self.position.y, self.position.z+1)
            possiblemoves6.position = (self.position.x-1, self.position.y, self.position.z+1)
            possiblemoves7.position = (self.position.x+1, self.position.y, self.position.z-1)
            possiblemoves8.position = (self.position.x, self.position.y, self.position.z-1)
            show_moves()
        else:
            self.color = color.gray  # Change la couleur pour feedback
            hide_moves()
#classe pour le fou
class Bishop(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        hide_moves()
        if self.color != color.red:
            reset()
            self.color = color.red  

            for i in range(-7, 8):

                pm3 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                pm4 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm5 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm6 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)


                line_points.extend([pm3, pm4, pm5, pm6])

        else:
            # La reine est rouge -> on la remet rose et on cache les moves
            self.color = color.cyan
            for pm in line_points:
                pm.visible = False
            line_points.clear()
#classe pour la tour
class Tower(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        hide_moves()   
        if self.color != color.red:
            reset()
            self.color = color.red  

            for i in range(-7, 8):
                pm1 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                pm2 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                pm7 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                pm8 = Move(model='cube', scale=(1, 1.9, 1), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)
                line_points.extend([pm1, pm2, pm7, pm8])

        else:
            # La reine est rouge -> on la remet rose et on cache les moves
            self.color = color.pink
            for pm in line_points:
                pm.visible = False
            line_points.clear()
#classe pour le cavalier
class Knight(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.name}")
        hide_moves()
        if self.color == color.yellow:
            reset()
            self.color = color.red  
            color_moves()
            possiblemoves.position = (self.position.x+1, self.position.y, self.position.z+2)
            possiblemoves2.position = (self.position.x-1, self.position.y, self.position.z+2)
            possiblemoves3.position = (self.position.x+1, self.position.y, self.position.z-2)
            possiblemoves4.position = (self.position.x-1, self.position.y, self.position.z-2)
            possiblemoves5.position = (self.position.x+2, self.position.y, self.position.z+1)
            possiblemoves6.position = (self.position.x-2, self.position.y, self.position.z+1)
            possiblemoves7.position = (self.position.x+2, self.position.y, self.position.z-1)
            possiblemoves8.position = (self.position.x-2, self.position.y, self.position.z-1)
            show_moves()
        else:
            self.color = color.yellow  # Change la couleur pour feedback
            hide_moves()
#classe pour le pion enemy
class EnemyPion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self):
        targets = ponarmy + [knight1, knight2, king, queen, bishop1, bishop2, tower1, tower2]
        if turn == 0:
            for target in targets:
                if target.position == self.position and self.color == color.blue:
                    self.visible = False
                    self.position = (1000, 1000, 1000)
#commandes pour debug        
def input(key):
    if key == 'escape':
        exit()
    
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
#debug
def enemy_at_position(pos):
    for e in enemyponarmy:
        if e.position == pos and e.visible:
            return e
    return None
#fonction pour racourcir le code
def reset():
    possiblemoves.visible = False
    possiblemoves2.visible = False
    possiblemoves3.visible = False
    possiblemoves4.visible = False
    possiblemoves5.visible = False
    possiblemoves6.visible = False
    possiblemoves7.visible = False
    possiblemoves8.visible = False
    for pon in ponarmy:
        pon.color = color.orange
    knight1.color = color.yellow
    knight2.color = color.yellow
    bishop1.color = color.cyan
    bishop2.color = color.cyan
    tower1.color = color.azure
    tower2.color = color.azure
    king.color = color.gray
    queen.color = color.pink
    for pm in line_points:
        pm.visible = False
    line_points.clear()
#fonction pour racourcir le code
def hide_moves():
    possiblemoves.visible = False
    possiblemoves2.visible = False
    possiblemoves3.visible = False
    possiblemoves4.visible = False
    possiblemoves5.visible = False
    possiblemoves6.visible = False
    possiblemoves7.visible = False
    possiblemoves8.visible = False
#fonction pour racourcir le code
def color_moves():
    possiblemoves.color = color.green
    possiblemoves2.color = color.green
    possiblemoves3.color = color.green
    possiblemoves4.color = color.green
    possiblemoves5.color = color.green
    possiblemoves6.color = color.green
    possiblemoves7.color = color.green
    possiblemoves8.color = color.green
#fonction pour racourcir le code
def show_moves():
    possiblemoves.visible = True
    possiblemoves2.visible = True
    possiblemoves3.visible = True
    possiblemoves4.visible = True
    possiblemoves5.visible = True
    possiblemoves6.visible = True
    possiblemoves7.visible = True
    possiblemoves8.visible = True
#sol
for x in range(taille):
    for z in range(taille):
        color_case = color.white if (x + z) % 2 == 0 else color.black
        Entity(
            model='cube',
            color=color_case,
            position=(x - offset, 0, z - offset),  # On décale pour centrer
            scale=1
        )
#pions enemis et alliés 1 a 3 directions
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
#cavaliers 8 positions
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
#fous et tours 4 directions
bishop1 = Bishop(
    model='cube',
    color=color.cyan,
    position=(-4+2, 1.5, -4),  # c1
    scale=(1, 2, 1)
    )
bishop2 = Bishop(
    model='cube',
    color=color.cyan,
    position=(-4+5, 1.5, -4),  # f1
    scale=(1, 2, 1)
    )
tower1 = Tower(
    model='cube',
    color=color.azure,
    position=(-4+0, 1.5, -4),  # a1
    scale=(1, 2, 1)
    )
tower2 = Tower(
    model='cube',
    color=color.azure,
    position=(-4+7, 1.5, -4),  # h1
    scale=(1, 2, 1)
    )
#roi et reine 8 directions
king = King(
    model='cube',
    color=color.gray,
    position=(-4+3, 1.5, -4),  # e1
    scale=(1, 2, 1)
    )
queen = Queen(
    model='cube',
    color=color.pink,
    position=(-4+4, 1.5, -4),  # d1
    scale=(1, 2, 1)
    )
#directionsdemouvements
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
#lancement du jeu
app.run()