from ursina import *
from math import *
from classes import *
from classes.ai_core import board_state_from_entities, AI_Core
import sys, os
import time

# These are *lists of armies*, each army contains pieces (objects)
# You should initialize these after creating the armies in main()
playerarmy = []
aiarmy = []
alltowers = []

ai_core = None  # global AI core instance
turn = 1
def main():
    global playerarmy, aiarmy, alltowers

    app = Ursina()
    window.fullscreen = False 

    camera.position = Vec3(3.5, 60, 3.5)
    camera.look_at(Vec3(3.5, 0, 3.5))
    camera.rotation_y = 90  # cleaner rotation setting

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
    moves()
    global ai_core
    global turn
    # Get current simplified board state from entities
    current_board_state = board_state_from_entities()

    # Create AI core if not already created or update the board state
    if ai_core is None:
        ai_core = AI_Core(current_board_state, max_depth=3)
    else:
        ai_core.board_state = current_board_state

    # Call AI to make a move at some condition (you can decide when)
    if turn == 0:
        ai_core.make_move()
        turn = 1
    
    if not hasattr(update, "last_print_time"):
        update.last_print_time = time.time()
    current_time = time.time()
    if current_time - update.last_print_time >= 8:
        taille = 8
        print("Grille 8x8 :")
        for z in range(taille - 1, -1, -1):  # corrected to 0-based indexing
            line = ''
            for x in range(taille):
                # Check AI pieces by priority order
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

                # Check player pieces
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

                # Check board tile at lower height (-1)
                tile = next((t for t in boardmap if t.position == (x, -1, z)), None)
                if tile:
                    line += tile.name + "  "
                else:
                    line += ".   "  # empty space

            print(line)
        update.last_print_time = current_time


def input(key):
    global turn
    if key == 'f':
        window.fullscreen = not window.fullscreen

    elif key == 'f5':
        restart_program()

    elif key == 'escape':
        exit()

    elif key == 'b':
        # Debug: print all pieces and move selected ones forward
        for army_group in alltowers:
            for army in army_group:
                for piece in army:
                    print(piece.name)
                    if "s" in piece.name:
                        piece.position += Vec3(0, 0, 1)
                        piece.name = piece.name.replace("s", "")
                        turn = 0


def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)


def moves():
    # Show possible moves (green cubes) for selected pieces
    for army_group in alltowers:
        for army in army_group:
            for piece in army:
                if piece.color == color.red:
                    # Simplified example: each piece shows one or two potential moves
                    pos = piece.position
                    name = piece.name

                    if name == "sT": #Rook
                        _show_move(pos + Vec3(0, 0, 1))
                    elif name == "sQ": # queen
                        _show_move(pos + Vec3(0, 0, 1))
                    elif name == "sK": # king
                        _show_move(pos + Vec3(0, 0, 1))
                        _show_move(pos + Vec3(0, 0, -1))
                    elif name == "sP": # pawn
                        _show_move(pos + Vec3(0, 0, 1))
                    elif name == "sC":  # Knight
                        _show_move(pos + Vec3(-1, 0, 2))
                        _show_move(pos + Vec3(1, 0, 2))
                    elif name == "sB": # bishop
                        _show_move(pos + Vec3(1, 0, 1))


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
