from ursina import *
from math import *
from classes import *
from classes.ai_core import board_state_from_entities, AI_Core
import sys, os
import time

playerarmy = []
aiarmy = []
alltowers = []

ai_core = None
turn = 1

def main():
    global playerarmy, aiarmy, alltowers

    app = Ursina()
    window.fullscreen = False

    camera.position = Vec3(3.5, 60, 3.5)
    camera.look_at(Vec3(3.5, 0, 3.5))
    camera.rotation_y = 90

    # Initialize board
    damier = Board()

    # Create player armies
    pawn = Pawnarmy()
    knight = Knightarmy()
    queen = Queenarmy()
    king = Kingarmy()
    bishop = Bishoparmy()
    tower = Towerarmy()

    # Create AI armies
    ai_pawn = Ai_Pawnarmy()
    ai_knight = Ai_Knightarmy()
    ai_queen = Ai_Queenarmy()
    ai_king = Ai_Kingarmy()
    ai_bishop = Ai_Bishoparmy()
    ai_tower = Ai_Towerarmy()

    # Assign to global armies for access in update and moves
    playerarmy = [towerarmies, queenarmies, knightarmies, pawnarmies, kingarmies, bishoparmies]
    aiarmy = [ai_bishoparmies, ai_kingarmies, aipawnarmies, ai_queenarmies, ai_towerarmies, ai_knightarmies]
    alltowers = [aiarmy, playerarmy]

    app.run()


def update():
    global ai_core, turn
    moves()

    current_board_state = board_state_from_entities()

    if ai_core is None:
        ai_core = AI_Core(current_board_state, max_depth=3)
    else:
        ai_core.board_state = current_board_state

    # IA joue

    if turn == 0:
        ai_core.make_move()
        handle_captures(0)  # L’IA vient de jouer
        turn = 1


    # Affichage console
    if not hasattr(update, "last_print_time"):
        update.last_print_time = time.time()
    current_time = time.time()
    if current_time - update.last_print_time >= 8:
        taille = 8
        print("Grille 8x8 :")
        for z in range(taille - 1, -1, -1):
            line = ''
            for x in range(taille):
                piece = (
                    next((a for a in ai_towerarmies if a.position == (x, 0, z)), None) or
                    next((a for a in ai_bishoparmies if a.position == (x, 0, z)), None) or
                    next((a for a in ai_knightarmies if a.position == (x, 0, z)), None) or
                    next((a for a in ai_queenarmies if a.position == (x, 0, z)), None) or
                    next((a for a in ai_kingarmies if a.position == (x, 0, z)), None) or
                    next((a for a in aipawnarmies if a.position == (x, 0, z)), None)
                )
                if piece:
                    line += piece.name + "    "
                    continue

                piece = (
                    next((t for t in towerarmies if t.position == (x, 0, z)), None) or
                    next((b for b in bishoparmies if b.position == (x, 0, z)), None) or
                    next((k for k in knightarmies if k.position == (x, 0, z)), None) or
                    next((q for q in queenarmies if q.position == (x, 0, z)), None) or
                    next((k for k in kingarmies if k.position == (x, 0, z)), None) or
                    next((p for p in pawnarmies if p.position == (x, 0, z)), None)
                )
                if piece:
                    line += piece.name + "    "
                    continue

                tile = next((t for t in boardmap if t.position == (x, -1, z)), None)
                if tile:
                    line += tile.name + "  "
                else:
                    line += ".   "

            print(line)
        update.last_print_time = current_time


def input(key):
    global turn
    if key == 'f':
        window.fullscreen = not window.fullscreen

    if key == 'f5':
        restart_program()

    if key == 'escape':
        exit()

    if key == 'b':
        for army_group in alltowers:
            for army in army_group:
                for piece in army:
                    if "s" in piece.name:
                        piece.position += Vec3(0, 0, 1)
                        piece.name = piece.name.replace("s", "")
                        if piece.color == color.red:
                            piece.color = color.orange
                        handle_captures(1)  # Le joueur vient de jouer
                        turn = 0



def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)


def handle_captures(last_turn):
    if last_turn == 1:  # Joueur vient de jouer, il peut capturer des bleus
        for ai_group in aiarmy:
            for ais in ai_group[:]:
                for pawn_group in playerarmy:
                    for pon in pawn_group:
                        if ais.position == pon.position:
                            ai_group.remove(ais)
                            destroy(ais, delay=0.2)
                            print("blue was killed", )

    elif last_turn == 0:  # IA vient de jouer, elle peut capturer des oranges
        for pawn_group in playerarmy:
            for pon in pawn_group[:]:
                for ai_group in aiarmy:
                    for ais in ai_group:
                        if ais.position == pon.position:
                            pawn_group.remove(pon)
                            destroy(pon, delay=0.2)
                            print( pon.name, "orange was killed")



def moves():
    for army_group in alltowers:
        for army in army_group:
            for piece in army:
                if piece.color == color.red:
                    pos = piece.position
                    name = piece.name

                    if name == "sT":
                        for dx in range(-1, 2):
                            for dz in range(-1, 2):
                                if (dx == 0) != (dz == 0):
                                    for dist in range(1, 8):
                                        _show_move(pos + Vec3(dx * dist, 0, dz * dist))

                    elif name == "sQ":
                        for dx in range(-1, 2):
                            for dz in range(-1, 2):
                                if dx != 0 or dz != 0:
                                    for dist in range(1, 8):
                                        _show_move(pos + Vec3(dx * dist, 0, dz * dist))

                    elif name == "sK":
                        for dx in range(-1, 2):
                            for dz in range(-1, 2):
                                if dx != 0 or dz != 0:
                                    _show_move(pos + Vec3(dx, 0, dz))

                    elif name == "sP":
                        _show_move(pos + Vec3(0, 0, 1))
                        if pos.z == 1:
                            _show_move(pos + Vec3(0, 0, 2))
                        _show_move(pos + Vec3(1, 0, 1))
                        _show_move(pos + Vec3(-1, 0, 1))

                    elif name == "sC":
                        for move in [
                            Vec3(1, 0, 2), Vec3(2, 0, 1), Vec3(-1, 0, 2), Vec3(-2, 0, 1),
                            Vec3(1, 0, -2), Vec3(2, 0, -1), Vec3(-1, 0, -2), Vec3(-2, 0, -1)
                        ]:
                            _show_move(pos + move)

                    elif name == "sB":
                        for dx in [-1, 1]:
                            for dz in [-1, 1]:
                                for dist in range(1, 8):
                                    _show_move(pos + Vec3(dx * dist, 0, dz * dist))


def _show_move(position):
    possible_move = Entity(
        model='cube',
        color=color.green,
        position=position,
        scale=1
    )
    destroy(possible_move, delay=0.2)


if __name__ == "__main__":
    main()
