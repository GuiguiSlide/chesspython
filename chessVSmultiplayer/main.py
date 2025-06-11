#importer les bibliothèques nécessaires
from copy import *
from ursina import *
from math import *
from ursina.sequence import * 
#comment on lance l'application 
app = Ursina()
bg_music = Audio('background_music.mp3', loop=True, autoplay=True)
bg_music.volume = 1
kill_sound = Audio('Kill.mp3', loop=False, autoplay=False )
move_self = Audio('move-self.mp3',Loop=False,autoplay=False)
kingdeath =Audio('kingdeath.wav',Loop=False,autoplay=False)
# Camera orbit settings
orbit_radius = 20
orbit_speed = 5  # degrees per second
orbit_center = Vec3(0, 20, 0)
angle = 0
camera_orbit_enabled = False
#nothinginfrontfixer
nothing_in_front_North = True#Go up ↑
nothing_in_front_South = True#Go down ↓
nothing_in_front_East = True#Go right →
nothing_in_front_West = True#Go left ←
nothing_in_front_NorthEast = True#Go up right
nothing_in_front_NorthWest = True#Go up left
nothing_in_front_SouthEast = True#Go down right
nothing_in_front_SouthWest = True#Go down left
#configurer la fenetre
window.borderless = True
window.fullscreen = False
window.title = 'Chess'
#taille pour le damier
taille = 8# Taille du damier
offset = taille // 2# Décalage pour centrer la grille autour de (0,0,0)
# liste pour stocker les pions alliés
ponarmy = []
# Liste pour stocker les pions ennemis
enemyponarmy = []
# Liste pour stocker les mouvements possibles
line_points = []
#liste pour les mouvements sans repetitions
possiblemoveslist = []
# liste pour les équipes
ally = ponarmy
enemy = enemyponarmy
# mets le tour au joueur
turn = bool
turn = True
#animation
class ChessPiece(Entity):

    def die(self):
        if self.name != 'king':
            kill_sound.play()
        self.animate_y(self.y + 7, duration=3, curve=curve.out_expo)
        self.animate_color(color.rgba(0,155,255,0), duration=3, curve=curve.linear)  # match durations
        invoke(self.set_death_position, delay=3)  # wait until animations done
    def set_death_position(self):
        self.visible = False
        self.position = (1500, 1500, 1500)
#classe pour les mouvements
class Move(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
        move_self.play()
        print(f"Tu as cliqué sur : {self.position}")
        global turn
        # Cache TOUS les moves verts présents dans line_points
        for pm in line_points:
            destroy(pm, delay=0.01)  
        line_points.clear()
        # Cache les 8 moves fixes si tu en as besoin
        hide_moves()
        # Cache aussi self (optionnel car self est dans line_points normalement)
        self.visible = False
        # Déplace les pièces selon leur couleur rouge
        if turn == True:
            for allies in ally:
                if allies.color == color.red:
                    allies.position = (self.position.x, self.position.y, self.position.z)
                    allies.color = color.white
                    turn = False
        else:
            for enemies in enemy:
                if enemies.color == color.red:
                    enemies.position = (self.position.x, self.position.y, self.position.z)
                    enemies.color = color.white
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
        if turn == True:
            for allies in ally:
                if (self.position.x, self.position.y, self.position.z) == Vec3(allies.position.x, allies.position.y, allies.position.z):
                    for enemyes in enemy:
                        if enemyes.name == king:
                            print("enemy win")
                            exit()
                    self.position = (1000, 1000, 1000)
            ###!faire la fonction pour la mort du roi
        else:
            for enemyes in enemy:
                if (self.position.x, self.position.y, self.position.z) == Vec3(enemyes.position.x, enemyes.position.y, enemyes.position.z):
                    for allies in ally:
                        if allies.name == king:
                            print("enemy win")
                            exit()
                    self.position = (1000, 1000, 1000)
            ###!faire la fonction pour la mort du roi
            
            #empecher la piece de sortir du damier
#classe pour le pion
class Pion(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        global doublemovefirst
        print(self.position,self.name)
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
                if self.position.z==-3:
                    pos_forward = (x, 0.5, z + 1)
                    pos_forward_double = (x, 0.5, z + 2)
                    if not enemy_at_position(pos_forward) and not any(pon.position == pos_forward for pon in ponarmy):
                        possiblemoves3.color = color.green
                        possiblemoves3.position = pos_forward
                        possiblemoves3.visible = True
                        possiblemoves4.color = color.green
                        possiblemoves4.position = pos_forward_double
                        possiblemoves4.visible = True
                else:
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
class Queen(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Detect clicks

    def on_click(self):
        print(self.position, self.name)
        hide_moves()
        if self.color != color.red:
            reset()
            self.color = color.red

            # Generate moves in each of the 8 directions
            self.generate_moves_in_direction(0, 1)    # North ↑
            self.generate_moves_in_direction(0, -1)   # South ↓
            self.generate_moves_in_direction(1, 0)    # East →
            self.generate_moves_in_direction(-1, 0)   # West ←
            self.generate_moves_in_direction(1, 1)    # NorthEast ↗
            self.generate_moves_in_direction(-1, 1)   # NorthWest ↖
            self.generate_moves_in_direction(1, -1)   # SouthEast ↘
            self.generate_moves_in_direction(-1, -1)  # SouthWest ↙

        else:
            self.color = color.white
            for pm in line_points:
                destroy(pm, delay=0.01)

    def generate_moves_in_direction(self, dx, dz):
        i = 1
        while i <= 7:
            target_pos = Vec3(self.position.x + dx * i, self.position.y, self.position.z + dz * i)
            obstacle_found = False

            for piece in ally + enemy:
                if piece.position == target_pos:
                    obstacle_found = True
                    if piece.color != self.color:  # enemy -> allow capture
                        pm = Move(model='sphere', scale=(0.5, 1.9, 0.5),
                                   position=target_pos, color=color.green, visible=True)
                        line_points.append(pm)
                    break  # stop after first piece found

            if not obstacle_found:
                pm = Move(model='sphere', scale=(0.5, 1.9, 0.5),
                           position=target_pos, color=color.green, visible=True)
                line_points.append(pm)
            else:
                break  # stop if blocked by any piece

            i += 1

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
class King(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            print(self.position,self.name)
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
            print(self.position,self.name)
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
class Bishop(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'

    def on_click(self):
        # Handle click: highlight possible moves
        print(self.position, self.name)
        hide_moves()

        if self.color != color.red:
            reset()
            self.color = color.red

            # Diagonal directions: (dx, dz) pairs
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dz in directions:
                self.generate_moves_in_direction(dx, dz)
        else:
            self.color = color.white
            for pm in line_points:
                destroy(pm, delay=0.01)

    def generate_moves_in_direction(self, dx, dz):
        # Starting 1 square away
        i = 1
        while i <= 7:
            target_pos = Vec3(self.position.x + i * dx, self.position.y, self.position.z + i * dz)
            obstacle_found = False

            for piece in ally + enemy:
                if piece.position == target_pos:
                    obstacle_found = True
                    if piece.color != self.color:
                        pm = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=target_pos, color=color.green, visible=True)
                        line_points.append(pm)
                    break

            if not obstacle_found:
                pm = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=target_pos, color=color.green, visible=True)
                line_points.append(pm)
            else:
                break  # Stop at first obstacle
            i += 1

    def update(self):
        dead(self)
        # Ensure collider only active for the right turn
        if (turn and self in enemy) or (not turn and self in ally):
            self.collider = None
        else:
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour la tour
class Tower(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'

    def on_click(self):
        print(self.position, self.name)
        hide_moves()

        if self.color != color.red:
            reset()
            self.color = color.red

            # Straight directions: (dx, dz) pairs
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dz in directions:
                self.generate_moves_in_direction(dx, dz)
        else:
            self.color = color.white
            for pm in line_points:
                destroy(pm, delay=0.01)

    def generate_moves_in_direction(self, dx, dz):
        i = 1
        while i <= 7:
            target_pos = Vec3(self.position.x + i * dx, self.position.y, self.position.z + i * dz)
            obstacle_found = False

            for piece in ally + enemy:
                if piece.position == target_pos:
                    obstacle_found = True
                    if piece.color != self.color:
                        pm = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=target_pos, color=color.green, visible=True)
                        line_points.append(pm)
                    break

            if not obstacle_found:
                pm = Move(model='sphere', scale=(0.5, 1.9, 0.5), position=target_pos, color=color.green, visible=True)
                line_points.append(pm)
            else:
                break  # Stop at first obstacle
            i += 1

    def update(self):
        dead(self)
        # Ensure collider only active for the right turn
        if (turn and self in enemy) or (not turn and self in ally):
            self.collider = None
        else:
            invoke(setattr, self, 'collider', 'box', delay=0.01)
#classe pour le cavalier
class Knight(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics

    def on_click(self):
        if turn == True:
            print(self.position,self.name)
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
            print(self.position,self.name)
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
class EnemyPion(ChessPiece):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'  # Permet de détecter les clics
    def on_click(self):
        if turn == False:
            print(self.position,self.name)
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
                if self.position.z==2:
                    pos_forward = (x, 0.5, z - 1)
                    pos_forward_double = (x, 0.5, z - 2)
                    if not enemy_at_position(pos_forward) and not any(pon.position == pos_forward for pon in ponarmy):
                        possiblemoves3.color = color.green
                        possiblemoves3.position = pos_forward
                        possiblemoves3.visible = True
                        possiblemoves4.color = color.green
                        possiblemoves4.position = pos_forward_double
                        possiblemoves4.visible = True
                else:
                    pos_forward = (x, 0.5, z - 1)
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
        if piece == self or not piece.visible:
            continue
        if piece.position == self.position:
            if piece.name == "king":
                kingdeath.play()
                if turn == True:
                    win.enabled = True
                    win.text = 'tu as perdu'
                else:
                    win.enabled = True
                    win.text = 'tu as gagné'

                invoke(exit,delay=5)
            else:
                kill_sound.play()
            print(self.name, "eaten", piece.name, "at", self.position)
            piece.die()  
#commandes pour debug
def input(key):
    global camera_orbit_enabled
    global orbit_speed
    if key == 'escape':
        exit()
    if key == 'f':  # fullscreen
        if not window.fullscreen:
            window.fullscreen = True
        else:
            window.fullscreen = False
    # Camera orbit speed control with held keys
    if held_keys['right arrow']:
        orbit_speed += 20
    elif held_keys['left arrow']:
        orbit_speed += -20
    else:
        decrease_speed()
    if key == 'b':  # debug button
        board_map = {}

        # Collect floor positions
        for e in scene.entities:
            if getattr(e, 'name', None) == 'floor' and hasattr(e, 'position'):
                pos = e.position
                if pos is not None:
                    x, z = int(pos.x), int(pos.z)
                    board_map[(x, z)] = '.'

        # Choose points safely (empty list fallback)
        points = line_points if line_points else possiblemoveslist or []

        # Mark moves
        for pm in points:
            pos = getattr(pm, 'position', None)
            if pos and pos != Vec3(1000, 1000, 1000):
                try:
                    x, z = int(pos.x), int(pos.z)
                    board_map[(x, z)] = 'M'
                except Exception as e:
                    print(f"Skipping invalid move position {pos}: {e}")

        # Mark allies
        for a in ally or []:
            pos = getattr(a, 'position', None)
            if pos and pos != Vec3(1500, 1500, 1500):
                try:
                    x, z = int(pos.x), int(pos.z)
                    board_map[(x, z)] = 'A'
                except Exception as e:
                    print(f"Skipping invalid ally position {pos}: {e}")

        # Mark enemies
        for en in enemy or []:
            pos = getattr(en, 'position', None)
            if pos and pos != Vec3(1500, 1500, 1500):
                try:
                    x, z = int(pos.x), int(pos.z)
                    board_map[(x, z)] = 'E'
                except Exception as e:
                    print(f"Skipping invalid enemy position {pos}: {e}")

        if not board_map:
            print("Board map is empty, nothing to display.")
            return

        all_positions = board_map.keys()

        # Limit board print size to avoid huge loops/crashes
        max_size = 50

        min_x = max(min(x for x, z in all_positions), -max_size)
        max_x = min(max(x for x, z in all_positions), max_size)
        min_z = max(min(z for x, z in all_positions), -max_size)
        max_z = min(max(z for x, z in all_positions), max_size)

        print("\nBoard View:")
        try:
            for z in range(max_z, min_z - 1, -1):
                row = ""
                for x in range(min_x, max_x + 1):
                    cell = board_map.get((x, z), ' ')
                    row += f" {cell} "
                print(row)
        except Exception as e:
            print("Error during board print:", e)


    if key == 'o':
        camera_orbit_enabled = not camera_orbit_enabled
        return
#debug
def enemy_at_position(pos, is_enemy=False): 
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
    for allies in ally:
        allies.color = color.white
    for enemies in enemy:
        enemies.color = color.white
    for pm in line_points:
        destroy(pm, delay=0.01)  
    for pml in possiblemoveslist:
        pml.position = (1000, 1000, 1000)
        pml.visible = False
#fonction pour racourcir le code
def hide_moves():
    for pm in possiblemoveslist:
        pm.visible = False
#fonction pour racourcir le code
def color_moves():
    for pm in possiblemoveslist:
        pm.color = color.green
#fonction pour racourcir le code
def show_moves():
    for pm in possiblemoveslist:
        pm.visible = True
# et la fonction update() est appelée à chaque frame, ce qui correspond à la boucle de jeu principale.
def update():
    if camera_orbit_enabled:
        orbit_camera()
    else:
        camera.position = Vec3(0, 30, 0)
        camera.rotation = Vec3(90,0,0)
        camera.look_at(Vec3(0, 0, 0))  # Regarde vers le centre du damier
        
    speedometer.text = orbit_speed
#des conneries
def decrease_speed():
    global orbit_speed
    
    # If speed is out of bounds → death
    if orbit_speed > 10000 or orbit_speed < -10000:
        print("you died of head trauma")
        win.enabled = True
        win.text = "you died of head trauma"
        invoke(exit, delay=5)
        return  # stop further calls
    
    # Else, slow down speed toward 5
    if orbit_speed > 5 or orbit_speed < -5:
        if orbit_speed < 5:
            orbit_speed += 1
        elif orbit_speed > 5:
            orbit_speed -= 1
        invoke(decrease_speed, delay=0.1)     
#sol
for x in range(taille):
    for z in range(taille):
        color_case = color.white if (x + z) % 2 == 0 else color.black
        Entity(
            model='cube',
            color=color_case,
            position=(x - offset, 0, z - offset),  # On décale pour centrer
            scale=1,
            name='floor'
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
    model='Tower',
    color=color.white,
    position=(-4+0, 0.5, 3),  # a1
    scale=(0.5, 1, 0.5)
    )
enemy.append(tower1enemy)
tower2enemy = Tower(
    texture='blackmarble',
    model='Tower',
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
possiblemoveslist.append(possiblemoves)
possiblemoves2 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves2)
possiblemoves3 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves3)
possiblemoves4 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves4)
possiblemoves5 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves5)
possiblemoves6 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves6)
possiblemoves7 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves7)
possiblemoves8 = Move(
    model='sphere',
    scale=(0.5, 1.9, 0.5)
)
possiblemoveslist.append(possiblemoves8)
#texte pour l'ecran de victoire
win = Text(
    text='tu as gagné',     # le texte à afficher
    position=(-0.25, 0.4),           # position à l'écran (x, y)
    scale=2,                        # taille du texte
    color=color.azure,              # couleur du texte                # fond derrière le texte
)
win.enabled=False
speedometer = Text(
    text=f"{orbit_speed}",
    origin=(-0.5, 0.5),  # Anchor point at top-left of the text
    position=(-0.85, 0.35), # Near the top-left of the screen
    scale=0.5,
    color=color.white
)
debugbutton = Text(
    text="B for MAP",
    origin=(-0.5, 0.5),  # Anchor point at top-left of the text
    position=(-0.8, 0.40),  # Near the top-left of the screen
    scale=0.5,
    color=color.yellow
)
debugbutton = Text(
    text="= O for orbit, ARROWS for orbit speed ",
    origin=(-0.5, 0.5),  # Anchor point at top-left of the text
    position=(-0.835, 0.35),  # Near the top-left of the screen
    scale=0.5,
    color=color.yellow
)
debugbutton = Text(
    text="ESCAPE to close the app",
    origin=(-0.5, 0.5),  # Anchor point at top-left of the text
    position=(-0.8, 0.3),  # Near the top-left of the screen
    scale=0.5,
    color=color.yellow
)
debugbutton = Text(
    text="F for fullscreen toggle",
    origin=(-0.5, 0.5),  # Anchor point at top-left of the text
    position=(-0.8, 0.25),  # Near the top-left of the screen
    scale=0.5,
    color=color.yellow
)

#lancement du jeu
app.run()