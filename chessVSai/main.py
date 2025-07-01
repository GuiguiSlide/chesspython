from ursina import *
from math import *
from classes import *
from classes.ai_core import board_state_from_entities, AI_Core
import sys, os
import time
from os.path import *
from panda3d.core import ConfigVariableInt

playerarmy = []
aiarmy = []
alltowers = []
move_indicators = []

orbit_radius = 20
orbit_speed = 5  # degrees per second
orbit_center = Vec3(3.5, 40, 3.5)
camera_orbit_enabled = False
angle = 0

selected_piece = None
ai_core = None
turn = 1
possible_move = None

ConfigVariableInt('win-size', 1536)
ConfigVariableInt('win-size', 864)

class Move(Entity):
    def __init__(self, *args, onclick=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.onclick = onclick
        self.is_move_indicator = True  # Unique flag for move indicators

    def on_click(self):
        global turn
        global handle_captures
        if self.onclick:
            self.onclick(self)
        handle_captures(1)  # Handle any captures that occur
        turn = 0  # Set the turn to 0 (likely switching to the other player)
        
def main():
    global playerarmy, aiarmy, alltowers

    app = Ursina(title="chessgamevsai", borderless=False)  # Show windowed bar at the top

    if exists('icon2.ico'):
        window.icon = 'icon2.ico'
    else:
        print("⚠️ Icône non trouvée à 'icon2.ico'")
    window.fullscreen = False
    window.size = (int(1536), int(864))
    
    camera.position = Vec3(3.5, 60, 3.5)
    camera.look_at(Vec3(3.5, 0, 3.5))

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
    current_board_state = board_state_from_entities()
    end()

    if camera_orbit_enabled:
        orbit_camera()
    else:
        camera.position = Vec3(3.5, 30, 3.5)
        camera.rotation = Vec3(90,0,0)
        camera.look_at(Vec3(3.5, 0, 3.5))  # Look at the center of the board

    for pon in playerarmy:
        for ally in pon:
            for move in move_indicators:
                if move.position == ally.position:
                    move_indicators.remove(move)
                    destroy(move, delay=0.001)

    if turn == 1:
        destroy(possible_move, delay=1)

    if ai_core is None:
        ai_core = AI_Core(current_board_state, max_depth=3)
    else:
        ai_core.board_state = current_board_state

    # AI plays
    if turn == 0:
        ai_core.make_move()
        handle_captures(0)  # AI just played
        turn = 1

    # Console display
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
                    next((c for c in knightarmies if c.position == (x, 0, z)), None) or
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

    # Promotion for player pawns
    for pawns in pawnarmies[:]:
        if pawns.position.z == 7:
            pawnarmies.remove(pawns)
            queenarmies.append(pawns)
            pawns.name = 'Q'

    # Promotion for AI pawns
    for aipawn in aipawnarmies[:]:
        if aipawn.position.z == 0:
            aipawnarmies.remove(aipawn)
            ai_queenarmies.append(aipawn)
            aipawn.name = 'Q'

def input(key):
    global selected_piece, turn
    global camera_orbit_enabled
    global orbit_speed
    if key == 'o':
        camera_orbit_enabled = not camera_orbit_enabled
        return

    if held_keys['right arrow']:
        orbit_speed += 20
    elif held_keys['left arrow']:
        orbit_speed += -20
    else:
        decrease_speed()
    if key == 'f':
        window.fullscreen = not window.fullscreen

    if key == 'f5':
        restart_program()

    if key == 'escape':
        exit()

    # Si c'est un roque, déplace aussi la tour


    if mouse.hovered_entity:
        entity = mouse.hovered_entity

        if key == 'left mouse down':
            # Select piece
            if hasattr(entity, 'color') and entity.color == color.white:
                selected_piece = entity
                resetcolors()
                clear_move_indicators()
                show_moves_for_piece(entity)
                entity.color = color.white

    # Move to selected square
    if getattr(entity, "is_move_indicator", False) and selected_piece:
        old_pos = selected_piece.position
        selected_piece.position = entity.position
        selected_piece.color = color.red
        selected_piece.has_moved = True  # ✅ Mark piece as moved

        # === Detect and Handle Castling ===
        if selected_piece.name.endswith("K"):
            print(f"[DEBUG] King moved from {old_pos} to {entity.position}")
            # King-side castling
            if old_pos == Vec3(4, 0, 0) and entity.position == Vec3(6, 0, 0):
                print("[DEBUG] King-side castling detected")
                rook = get_piece_at(Vec3(7, 0, 0))
                print(f"[DEBUG] King-side rook to move: {rook}")
                if rook:
                    rook.position = Vec3(5, 0, 0)
                    rook.has_moved = True
                    print("[DEBUG] King-side rook moved to f1")
            # Queen-side castling
            elif old_pos == Vec3(4, 0, 0) and entity.position == Vec3(2, 0, 0):
                print("[DEBUG] Queen-side castling detected")
                rook = get_piece_at(Vec3(0, 0, 0))
                print(f"[DEBUG] Queen-side rook to move: {rook}")
                if rook:
                    rook.position = Vec3(3, 0, 0)
                    rook.has_moved = True
                    print("[DEBUG] Queen-side rook moved to d1")

        clear_move_indicators()
        handle_captures(1)
        turn = 0
        selected_piece = None
        entity.color = color.red


def orbit_camera():
    global angle
    camera.look_at(orbit_center)
    angle += time.dt * orbit_speed
    rad = radians(angle)

    # New camera position around center
    camera.x = orbit_center.x + orbit_radius * cos(rad)
    camera.z = orbit_center.z + orbit_radius * sin(rad)
    camera.y = 40  # Fixed height

    # Calculate yaw so the camera faces the center
    dx = orbit_center.x - camera.x
    dz = orbit_center.z - camera.z
    yaw = degrees(atan2(dx, dz))  # atan2(x, z), not z, x!

    # Keep your custom downward tilt (pitch = 30°)
    camera.rotation = (60, yaw, 0)

def end():
    player_king_exists = False
    for pawn_group in playerarmy:
        for pon in pawn_group:
            if "K" in getattr(pon, "name", ""):
                player_king_exists = True
                break
        if player_king_exists:
            break
    if not player_king_exists:
        print('you lose','ai won')
        exit()

    ai_king_exists = False
    for ai_group in aiarmy:
        for ais in ai_group:
            if "K" in getattr(ais, "name", ""):
                ai_king_exists = True
                break
        if ai_king_exists:
            break
    if not ai_king_exists:
        print("ai lose",'you win')
        exit()

def decrease_speed():
    global orbit_speed

    # If speed is out of bounds → death
    if orbit_speed > 10000 or orbit_speed < -10000:
        print("you died of head trauma")
        invoke(exit, delay=5)
        return  # stop further calls

    # Else, slow down speed toward 5
    if orbit_speed > 5 or orbit_speed < -5:
        if orbit_speed < 5:
            orbit_speed += 1
        elif orbit_speed > 5:
            orbit_speed -= 1
        invoke(decrease_speed, delay=0.1)

def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)

def handle_captures(last_turn):
    if last_turn == 1:  # Player just played, can capture blues
        for ai_group in aiarmy:
            for ais in ai_group[:]:
                for pawn_group in playerarmy:
                    for pon in pawn_group:
                        if ais.position == pon.position:
                            ai_group.remove(ais)
                            destroy(ais, delay=0.2)
                            print("black was killed", )

    elif last_turn == 0:  # AI just played, can capture whites
        for pawn_group in playerarmy:
            for pon in pawn_group[:]:
                for ai_group in aiarmy:
                    for ais in ai_group:
                        if ais.position == pon.position:
                            pawn_group.remove(pon)
                            destroy(pon, delay=0.2)
                            print(pon.name, "white was killed")

def resetcolors():
    for army_group in alltowers:
        for army in army_group:
            for other in army:
                if other.color == color.red:
                    other.color = color.white

def show_moves_for_piece(piece):
    def is_on_board(vec):
        return 0 <= vec.x < 8 and 0 <= vec.z < 8

    def is_friendly_piece_at(vec):
        for army_group in alltowers:
            for army in army_group:
                for other in army:
                    if other.position == vec and other.color == color.red:
                        return True
        return False

    def is_any_piece_at(vec):
        for army_group in alltowers:
            for army in army_group:
                for other in army:
                    if other.position == vec:
                        return True
        return False

    pos = piece.position
    name = piece.name

    if name.endswith("T"):
        for dx, dz in [(1,0), (-1,0), (0,1), (0,-1)]:
            for dist in range(1, 8):
                target = pos + Vec3(dx * dist, 0, dz * dist)
                if not is_on_board(target):
                    break
                if is_friendly_piece_at(target):
                    break
                _show_move(target)
                if is_any_piece_at(target):
                    break

    if name.endswith("K"):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if dx != 0 or dz != 0:
                    target = pos + Vec3(dx, 0, dz)
                    if is_on_board(target) and not is_friendly_piece_at(target):
                        _show_move(target)

        # === Castling Logic for WHITE King ===
        if pos == Vec3(4, 0, 0) and not piece.has_moved:
            print("[DEBUG] King at e1, checking castling possibilities")
            # King-side castling (e1 -> g1)
            rook_ks = get_piece_at(Vec3(7, 0, 0))
            print(f"[DEBUG] King-side rook: {rook_ks}")
            if rook_ks and rook_ks.name.endswith("T") and not rook_ks.has_moved:
                print("[DEBUG] King-side rook has not moved and is correct type")
                empty_ks = [not is_any_piece_at(Vec3(x, 0, 0)) for x in [5, 6]]
                print(f"[DEBUG] King-side empty squares [f1,g1]: {empty_ks}")
                if all(empty_ks):
                    print("[DEBUG] King-side castling is possible, showing move to g1")
                    _show_move(Vec3(6, 0, 0))  # g1

            # Queen-side castling (e1 -> c1)
            rook_qs = get_piece_at(Vec3(0, 0, 0))
            print(f"[DEBUG] Queen-side rook: {rook_qs}")
            if rook_qs and rook_qs.name.endswith("T") and not rook_qs.has_moved:
                print("[DEBUG] Queen-side rook has not moved and is correct type")
                empty_qs = [not is_any_piece_at(Vec3(x, 0, 0)) for x in [1, 2, 3]]
                print(f"[DEBUG] Queen-side empty squares [b1,c1,d1]: {empty_qs}")
                if all(empty_qs):
                    print("[DEBUG] Queen-side castling is possible, showing move to c1")
                    _show_move(Vec3(2, 0, 0))  # c1


                        
    if name.endswith("Q"):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                if dx != 0 or dz != 0:
                    for dist in range(1, 8):
                        target = pos + Vec3(dx * dist, 0, dz * dist)
                        if not is_on_board(target) or is_friendly_piece_at(target):
                            break
                        _show_move(target)
                        if is_any_piece_at(target):
                            break

    if name.endswith("P"):
        is_white = piece.color == color.white
        direction = 1 if is_white else -1
        start_row = 1 if is_white else 6

        forward = pos + Vec3(0, 0, direction)
        if is_on_board(forward) and not is_any_piece_at(forward):
            _show_move(forward)
            if pos.z == start_row:
                double_forward = pos + Vec3(0, 0, 2 * direction)
                if is_on_board(double_forward) and not is_any_piece_at(double_forward):
                    _show_move(double_forward)

        # Check diagonals
        # Check right diagonal for capture
        for dx in (1, 1):
            diag = pos + Vec3(dx, 0, direction)
            if is_on_board(diag):
                enemy = get_piece_at(diag)
                if enemy and enemy.color == piece.color:
                    _show_move(diag)

        # Check left diagonal for capture
        for dx in (1, -1):
            diag = pos + Vec3(dx, 0, direction)
            if is_on_board(diag):
                enemy = get_piece_at(diag)
                if enemy and enemy.color == piece.color:
                    _show_move(diag)

    if name.endswith("C"):
        for move in [
            Vec3(1, 0, 2), Vec3(2, 0, 1), Vec3(-1, 0, 2), Vec3(-2, 0, 1),
            Vec3(1, 0, -2), Vec3(2, 0, -1), Vec3(-1, 0, -2), Vec3(-2, 0, -1)
        ]:
            target = pos + move
            if is_on_board(target) and not is_friendly_piece_at(target):
                _show_move(target)

    if name.endswith("B"):
        for dx in [-1, 1]:
            for dz in [-1, 1]:
                for dist in range(1, 8):
                    target = pos + Vec3(dx * dist, 0, dz * dist)
                    if not is_on_board(target) or is_friendly_piece_at(target):
                        break
                    _show_move(target)
                    if is_any_piece_at(target):
                        break

def get_piece_at(position):
    for army_group in alltowers:
        for army in army_group:
            for piece in army:
                if piece.position == position:
                    return piece
    return None

def _show_move(position):
    global move_indicators
    move = Move(
        model='cube',
        color=color.green,
        position=position,
        scale=1,
        collider='box'
    )
    move_indicators.append(move)

def clear_move_indicators():
    # Iterate through all piece armies (kings, towers, queens, bishops, knights, pawns)
    for pawn_group in playerarmy:
        for pon in pawn_group[:]:
            for ai_group in aiarmy:
                for ais in ai_group:
                    pon.color = color.white  # Change the piece's color to white
    global move_indicators
    for move in move_indicators:
        destroy(move)
    move_indicators = []


if __name__ == "__main__":
    main()
