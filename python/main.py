#importer les bibliothèques nécessaires
from copy import *
from ursina import *
import random
from math import sin, cos, radians,atan2, degrees
#comment on lance l'application
app = Ursina()
# Camera orbit settings
orbit_radius = 20
orbit_speed = 5  # degrees per second
orbit_center = Vec3(0, 0, 0)
angle = 0
camera_orbit_enabled = True
#configurer la fenetre
window.borderless = True
window.fullscreen = False
window.title = 'Chess'
#taille pour le damier
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
# Position de la caméra
        # Orientation vers le bas
# liste pour stocker les pions alliés
ponarmy = []
# Liste pour stocker les pions ennemis
enemyponarmy = []
# Liste pour stocker les mouvements possibles
line_points = []
# mets le tour au joueur
ally = ponarmy
enemy = enemyponarmy
turn = bool
turn = True

#classe pour les mouvements
class Move(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
        print(f"Tu as cliqué sur : {self.position}")
        global turn
        # Cache TOUS les moves verts présents dans line_points
        for pm in line_points:
            destroy(pm, delay=0.01)  
  # Move it far away to "hide"
         # Schedule destruction shortly after

        line_points.clear()

        # Cache les 8 moves fixes si tu en as besoin
        hide_moves()

        # Cache aussi self (optionnel car self est dans line_points normalement)
        self.visible = False

        # Déplace les pièces selon leur couleur rouge
        if turn == True:
            if knight1.color == color.red:
                knight1.position = (self.position.x, self.position.y, self.position.z)
                knight1.color = color.white
                turn = False
            if knight2.color == color.red:
                knight2.position = (self.position.x, self.position.y, self.position.z)
                knight2.color = color.white
                turn = False
            if tower1.color == color.red:
                tower1.position = (self.position.x, self.position.y, self.position.z)
                tower1.color = color.white
                turn = False
            if tower2.color == color.red:
                tower2.position = (self.position.x, self.position.y, self.position.z)
                tower2.color = color.white
                turn = False
            if bishop1.color == color.red:
                bishop1.position = (self.position.x, self.position.y, self.position.z)
                bishop1.color = color.white
                turn = False
            if bishop2.color == color.red:
                bishop2.position = (self.position.x, self.position.y, self.position.z)
                bishop2.color = color.white
                turn = False
            for pon in ponarmy:
                if pon.color == color.red:
                    pon.position = (self.position.x, self.position.y, self.position.z)
                    pon.color = color.white
                    turn = False
            if king.color == color.red:
                king.position = (self.position.x, self.position.y, self.position.z)
                king.color = color.white
                turn = False
            if queen.color == color.red:
                queen.position = (self.position.x, self.position.y, self.position.z)
                queen.color = color.white
                turn = False
        else:
            for enemypon in enemyponarmy:
                if enemypon.color == color.red:
                    enemypon.position = (self.position.x, self.position.y, self.position.z)
                    enemypon.color = color.white
                    turn = True
            if queenenemy.color == color.red:
                queenenemy.position = (self.position.x, self.position.y, self.position.z)
                queenenemy.color = color.white
                turn = True
            if kingenemy.color == color.red:
                kingenemy.position = (self.position.x, self.position.y, self.position.z)
                kingenemy.color = color.white
                turn = True
            if knight1enemy.color == color.red:
                knight1enemy.position = (self.position.x, self.position.y, self.position.z)
                knight1enemy.color = color.white
                turn = True
            if knight2enemy.color == color.red:
                knight2enemy.position = (self.position.x, self.position.y, self.position.z)
                knight2enemy.color = color.white
                turn = True
            if tower1enemy.color == color.red:
                tower1enemy.position = (self.position.x, self.position.y, self.position.z)
                tower1enemy.color = color.white
                turn = True
            if tower2enemy.color == color.red:
                tower2enemy.position = (self.position.x, self.position.y, self.position.z)
                tower2enemy.color = color.white
                turn = True
            if bishop1enemy.color == color.red:
                bishop1enemy.position = (self.position.x, self.position.y, self.position.z)
                bishop1enemy.color = color.white
                turn = True
            if bishop2enemy.color == color.red:
                bishop2enemy.position = (self.position.x, self.position.y, self.position.z)
                bishop2enemy.color = color.white
                turn = True
            
    def update(self):
        # Limite du damier en X
        if self.position.x < -4 or self.position.x > 3:
            self.position = (1000, 1000, 1000)
            return

        # Limite du damier en Z
        if self.position.z < -4 or self.position.z > 3:
            self.position = (1000, 1000, 1000)
            return

        # Hauteur fixe (évite que le Y soit modifié, sauf si voulu)
        if self.position.y != 0.5:
            self.position = (1000, 1000, 1000)
            return

        # Vérifie si la position du mouvement est égale à mon pion
        # Empêcher le mouvement sur une case occupée par une pièce alliée
        if turn == True:
            for pon in ponarmy:
                if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(pon.position.x, pon.position.y, pon.position.z):
                    self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(knight1.position.x, knight1.position.y, knight1.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(knight2.position.x, knight2.position.y, knight2.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(king.position.x, king.position.y, king.position.z):
                self.position = (1000, 1000, 1000)
                print("Tu as gagné bleu")
                exit()

            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(queen.position.x, queen.position.y, queen.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(bishop1.position.x, bishop1.position.y, bishop1.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(bishop2.position.x, bishop2.position.y, bishop2.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(tower1.position.x, tower1.position.y, tower1.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(tower2.position.x, tower2.position.y, tower2.position.z):
                self.position = (1000, 1000, 1000)
        else:
            for enemypon in enemyponarmy:
                if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(enemypon.position.x, enemypon.position.y, enemypon.position.z):
                    self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(knight1enemy.position.x, knight1enemy.position.y, knight1enemy.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(knight2enemy.position.x, knight2enemy.position.y, knight2enemy.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(kingenemy.position.x, kingenemy.position.y, kingenemy.position.z):
                self.position = (1000, 1000, 1000)
                print("Tu as gagné white")
                exit()

            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(queenenemy.position.x, queenenemy.position.y, queenenemy.position.z):    
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(bishop1enemy.position.x, bishop1enemy.position.y, bishop1enemy.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(bishop2enemy.position.x, bishop2enemy.position.y, bishop2enemy.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(tower1enemy.position.x, tower1enemy.position.y, tower1enemy.position.z):
                self.position = (1000, 1000, 1000)
            if Vec3(self.position.x, self.position.y, self.position.z) == Vec3(tower2enemy.position.x, tower2enemy.position.y, tower2enemy.position.z):
                self.position = (1000, 1000, 1000)
            #empecher la piece de sortir du damier
#classe pour le pion
class Pion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        print(f"Tu as cliqué sur : {self.position}")
        if turn == True:
            # Masquer toutes les cases de déplacement possibles
            hide_moves()
            #reinitialisation
            if self.color == color.white:
                reset()
                self.color = color.red  

                # Position actuelle du pion
                x, y, z = self.position
                
                # 1) Vérifier capture sur diagonale avant-gauche (x-1, y, z+1)
                pos_diag_left = (x - 1, 0.5, z + 1)
                if enemy_at_position(pos_diag_left, is_enemy=False):
                    possiblemoves.color = color.green
                    possiblemoves.position = pos_diag_left
                    possiblemoves.visible = True
                
                # 2) Vérifier capture sur diagonale avant-droite (x+1, y, z+1)
                pos_diag_right = (x + 1, 0.5, z + 1)
                if enemy_at_position(pos_diag_right, is_enemy=False):
                    possiblemoves2.color = color.green
                    possiblemoves2.position = pos_diag_right
                    possiblemoves2.visible = True

                # 3) Vérifier déplacement normal vers l'avant (x, y, z+1) sans ennemi
                pos_forward = (x, 0.5, z + 1)
                if not enemy_at_position(pos_forward) and not any(pon.position == pos_forward for pon in ponarmy):
                    possiblemoves3.color = color.green
                    possiblemoves3.position = pos_forward
                    possiblemoves3.visible = True

            else:
                # Si on clique sur un pion rouge (sélectionné), on le désélectionne
                self.color = color.white  
                possiblemoves.visible = False
                possiblemoves2.visible = False
                possiblemoves3.visible = False
    def update(self):
        dead(self)
        if turn == False:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour la reine  
class Queen(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            hide_moves()
            if self.color != color.red:
                # La reine n'est pas rouge -> on la passe en rouge
                reset()
                self.color = color.red  

                for i in range(-7, 8):
                    pm1 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                    pm2 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm3 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm4 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm5 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm6 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm7 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm8 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)

                    line_points.extend([pm1, pm2, pm3, pm4, pm5, pm6, pm7, pm8])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01) 
        else: 
            print(f"Tu as cliqué sur : {self.name} enemy")
            hide_moves()
            if self.color != color.red:
                # La reine n'est pas rouge -> on la passe en rouge
                reset()
                self.color = color.red  

                for i in range(-7, 8):
                    pm1 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                    pm2 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm3 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm4 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm5 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm6 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm7 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm8 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)

                    line_points.extend([pm1, pm2, pm3, pm4, pm5, pm6, pm7, pm8])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01) 
    def update(self):
        dead(self)
        if turn and self not in ally:
            self.collider = None
        else:
            invoke(setattr, self, 'collider', 'box', delay=0.01)
        if not turn and self not in enemy:
            self.collider = None
        else:
            invoke(setattr, self, 'collider', 'box', delay=0.01)
# classe pour le roi
class King(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            if self.color == color.white:
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
                self.color = color.white  # Change la couleur pour feedback
                hide_moves()
        else:
            print(f"Tu as cliqué sur : {self.name} enemy")
            if self.color == color.white:
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
                self.color = color.white  # Change la couleur pour feedback
                hide_moves()
    def update(self):
        dead(self)
        if turn == False and self in ally:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
        if turn == True and self in enemy:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour le fou
class Bishop(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            hide_moves()
            if self.color != color.red:
                reset()
                self.color = color.red  

                for i in range(-7, 8):
                    pm3 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm4 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm5 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm6 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    line_points.extend([pm3, pm4, pm5, pm6])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01)
        else: 
            print(f"Tu as cliqué sur : {self.name} enemy")
            hide_moves()
            if self.color != color.red:
                reset()
                self.color = color.red  

                for i in range(-7, 8):

                    pm3 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm4 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm5 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm6 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z + i), color=color.green, visible=True)


                    line_points.extend([pm3, pm4, pm5, pm6])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01)
    def update(self):
        dead(self)
        if turn == False and self in ally:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01) 
        if turn == True and self in enemy:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01) 
#classe pour la tour
class Tower(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            hide_moves()   
            if self.color != color.red:
                reset()
                self.color = color.red  

                for i in range(-7, 8):
                    pm1 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                    pm2 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm7 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm8 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)
                    line_points.extend([pm1, pm2, pm7, pm8])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01) 
        else:
            print(f"Tu as cliqué sur : {self.name} enemy")
            hide_moves()   
            if self.color != color.red:
                reset()
                self.color = color.red  

                for i in range(-7, 8):
                    pm1 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x + i, self.position.y, self.position.z), color=color.green, visible=True)
                    pm2 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z + i), color=color.green, visible=True)
                    pm7 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x, self.position.y, self.position.z - i), color=color.green, visible=True)
                    pm8 = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=(self.position.x - i, self.position.y, self.position.z), color=color.green, visible=True)
                    line_points.extend([pm1, pm2, pm7, pm8])

            else:
                # La reine est rouge -> on la remet rose et on cache les moves
                self.color = color.white
                for pm in line_points:
                    destroy(pm, delay=0.01) 
    def update(self):
        dead(self)
        if turn == False and self in ally:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
        if turn == True and self in enemy:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour le cavalier
class Knight(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            hide_moves()
            if self.color == color.white:
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
                self.color = color.white  # Change la couleur pour feedback
                hide_moves()
        else:
            print(f"Tu as cliqué sur : {self.name} enemy")
            hide_moves()
            if self.color == color.white:
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
                self.color = color.white  # Change la couleur pour feedback
                hide_moves()
    def update(self):
        dead(self)
        if turn == False and self in ally:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
        if turn == True and self in enemy:
            self.collider = None
        else :
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour le pion enemy
class EnemyPion(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
        if turn == False:
            # Masquer toutes les cases de déplacement possibles
            hide_moves()
            #reinitialisation
            if self.color == color.white:
                reset()
                self.color = color.red  

                # Position actuelle du pion
                x, y, z = self.position
                    
                # arrière-gauche
                pos_diag_left = (x - 1, y, z - 1)
                if enemy_at_position(pos_diag_left, is_enemy=True):
                    possiblemoves.color = color.green
                    possiblemoves.position = pos_diag_left
                    possiblemoves.visible = True

                # arrière-droite
                pos_diag_right = (x + 1, y, z - 1)
                if enemy_at_position(pos_diag_right, is_enemy=True):
                    possiblemoves2.color = color.green
                    possiblemoves2.position = pos_diag_right
                    possiblemoves2.visible = True

                # 3) Vérifier déplacement normal vers l'arrière (x, y, z-1) sans ennemi
                pos_backward = (x, y, z - 1)
                if not enemy_at_position(pos_backward) and not any(enemypon.position == pos_backward for enemypon in enemyponarmy):
                    possiblemoves3.color = color.green
                    possiblemoves3.position = pos_backward
                    possiblemoves3.visible = True

            else:
                # Si on clique sur un pion rouge (sélectionné), on le désélectionne
                self.color = color.white
                possiblemoves.visible = False
                possiblemoves2.visible = False
                possiblemoves3.visible = False

    def update(self):
        dead(self)
        if turn == True:
            self.collider = None
        else:
            invoke(setattr, self, 'collider', 'box', delay=0.01)
# Fonction pour faire orbiter la caméra autour du damier
def orbit_camera():
    global angle
    camera.look_at(orbit_center)
    angle += time.dt * orbit_speed
    rad = radians(angle)

    # New camera position around center
    camera.x = orbit_center.x + orbit_radius * cos(rad)
    camera.z = orbit_center.z + orbit_radius * sin(rad)
    camera.y = 25  # Fixed height
      # Look at the center of the board
    # Calculate yaw so the camera faces the center
    dx = orbit_center.x - camera.x
    dz = orbit_center.z - camera.z
    yaw = degrees(atan2(dx, dz))  # atan2(x, z), not z, x!

    # Keep your custom downward tilt (pitch = 30°)
    camera.rotation = (50, yaw, 0)
#definir la mort
def dead(self):
    global ally
    global enemy

    target_list = enemy if not turn else ally

    for piece in target_list:
        # Vérifie qu'on ne se compare pas à soi-même
        if piece != self and piece.position == self.position:
            piece.visible = False
            piece.position = (1500, 1500, 1500)                        
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
        print(possiblemoves.position)
        print(possiblemoves2.position)
        global camera_orbit_enabled
    if key == 'o':
        camera_orbit_enabled = not camera_orbit_enabled

        return
#debug
def enemy_at_position(pos, is_enemy=False):
    """
    Renvoie une pièce ennemie à la position donnée, 
    en fonction du camp du pion appelant.
    
    :param pos: Position à vérifier
    :param is_enemy: False si appelé par un pion joueur, True si appelé par un pion ennemi
    """
    
    if is_enemy:
        for p in ponarmy:
            if p.position == pos and p.visible:
                return p
    else:
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
        pon.color = color.white
    knight1.color = color.white
    knight2.color = color.white
    bishop1.color = color.white
    bishop2.color = color.white
    tower1.color = color.white
    tower2.color = color.white
    king.color = color.white
    queen.color = color.white
    for enemypon in enemyponarmy:
        enemypon.color = color.white
    knight1enemy.color = color.white
    knight2enemy.color = color.white
    bishop1enemy.color = color.white
    bishop2enemy.color = color.white
    tower1enemy.color = color.white
    tower2enemy.color = color.white
    kingenemy.color = color.white
    queenenemy.color = color.white
    for pm in line_points:
        destroy(pm, delay=0.01)  
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
def update():
    if camera_orbit_enabled:
        orbit_camera()
    else:
        camera.position = Vec3(0, 30, 0)
        camera.look_at(Vec3(0, 0, 0))  # Regarde vers le centre du damier
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
        texture='whitemarble',
        model='Pawn',
        position=(x-4, 0.5, -3),  # Ligne 2 (rangée des pions)
        scale=(0.5, 1, 0.5),
        name=f'pon{x}'
        )
    ponarmy.append(pon)

    enemypon = EnemyPion(
        texture='blackmarble',
        model='Pawn',
        color=color.white,
        position=(x-4, 0.5, 2),  # Ligne 7 (rangée des pions adverses)
        scale=(0.5, 1, 0.5),
        name=f'enemypon{x}'
        )
    enemyponarmy.append(enemypon)  
#alliés
knight1 = Knight(
    texture='whitemarble',
    model='Knight',
    color=color.white,
    position=(-3, 0.5, -4),  # b1
    scale=(0.5, 1, 0.5)
    )
ally.append(knight1)
knight2 = Knight(
    texture='whitemarble',
    model='Knight',
    color=color.white,
    position=(-4+6, 0.5, -4),  # g1
    scale=(0.5, 1, 0.5)
    )
ally.append(knight2)
bishop1 = Bishop(
    texture='whitemarble',
    model='Bishop',
    color=color.white,
    position=(-4+2, 0.5, -4),  # c1
    scale=(0.5, 1, 0.5)
    )
ally.append(bishop1)
bishop2 = Bishop(
    texture='whitemarble',
    model='Bishop',
    color=color.white,
    position=(-4+5, 0.5, -4),  # f1
    scale=(0.5, 1, 0.5)
    )
ally.append(bishop2)
tower1 = Tower(
    texture='whitemarble',
    model='tower',
    color=color.white,
    position=(-4+0, 0.5, -4),  # a1
    scale=(0.5, 1, 0.5)
    )
ally.append(tower1)
tower2 = Tower(
    texture='whitemarble',
    model='tower',
    color=color.white,
    position=(-4+7, 0.5, -4),  # h1
    scale=(0.5, 1, 0.5)
    )
ally.append(tower2)
king = King(
    texture='whitemarble',
    model='King',
    color=color.white,
    position=(-4+4, 0.5, -4),  # e1
    scale=(0.5, 1, 0.5)
    )
ally.append(king)
queen = Queen(
    texture='whitemarble',
    model='Queen',
    color=color.white,
    position=(-4+3, 0.5, -4),  # d1
    scale=(0.5, 1, 0.5)
    )
ally.append(queen)
#enemis
knight1enemy = Knight(
    model='Knight',
    texture='blackmarble',
    color=color.white,
    position=(-3, 0.5, 3),  # b1
    scale=(0.5, 1, 0.5),
    rotation=(0, 180, 0)
    )
enemy.append(knight1enemy)
knight2enemy = Knight(
    texture='blackmarble',
    model='Knight',
    color=color.white,
    position=(-4+6, 0.5, 3),  # g1
    scale=(0.5, 1, 0.5),
    rotation=(0, 180, 0)
    )
enemy.append(knight2enemy)
bishop1enemy = Bishop(
    texture='blackmarble',
    model='Bishop',
    color=color.white,
    position=(-4+2, 0.5, 3),  # c1
    scale=(0.5, 1, 0.5),
    rotation=(0, 180, 0)
    )
enemy.append(bishop1enemy)
bishop2enemy = Bishop(
    texture='blackmarble',
    model='Bishop',
    color=color.white,
    position=(-4+5, 0.5, 3),  # f1
    scale=(0.5, 1, 0.5)
    )
enemy.append(bishop2enemy)
tower1enemy = Tower(
    texture='blackmarble',
    model='tower',
    color=color.white,
    position=(-4+0, 0.5, 3),  # a1
    scale=(0.5, 1, 0.5)
    )
enemy.append(tower1enemy)
tower2enemy = Tower(
    texture='blackmarble',
    model='tower',
    color=color.white,
    position=(-4+7, 0.5, 3),  # h1
    scale=(0.5, 1, 0.5)
    )
enemy.append(tower2enemy)
kingenemy = King(
    model='King',
    color=color.white,
    position=(-4+4, 0.5, 3),  # e1
    scale=(0.5, 1, 0.5),
    texture='blackmarble',
    )
enemy.append(kingenemy)
queenenemy = Queen(
    model='queen',
    texture='blackmarble',
    color=color.white,  # ← so texture is visible
    position=(-1, 0.5, 3),  # d1
    scale=(0.5, 1, 0.5)
)
enemy.append(queenenemy)
#directionsdemouvements
possiblemoves = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves2 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves3 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves4 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves5 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves6 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves7 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoves8 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
#lancement du jeu
app.run()