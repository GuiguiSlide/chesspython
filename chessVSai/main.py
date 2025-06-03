from ursina import *
from math import *
from classes import *
import sys, os


def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)
def main():
    app = Ursina()
    window.fullscreen = True 
    camera.position = Vec3(3.5,60,3.5)
    camera.look_at((3.5, 0, 3.5))
    camera.rotation.y=(90)
    damier = Board() 
    pawn = Pawnarmy()
    knight = Knightarmy()
    pawn = Pawnarmy()
    knight = Knightarmy()
    queen = Queenarmy()
    king = Kingarmy()
    bishop = Bishoparmy()
    tower = Towerarmy()
    ai_pawn = Ai_Pawnarmy()
    ai_knight = Ai_Knightarmy()
    ai_queen = Ai_Queenarmy()
    ai_king = Ai_Kingarmy()
    ai_bishop = Ai_Bishoparmy()
    ai_tower = Ai_Towerarmy()
    app.run()

def update():

    if held_keys['a']:
        pass
        
def input(key):
    if key == 'space':
        taille = 8
        print("Grille 8x8 inversée :")
        for z in range(taille):
            line = ''
            for x in range(taille):
            # AI pieces
                ai_tower = next((a for a in ai_towerarmies if a.position == (x, 0, z)), None)
                if ai_tower:
                    line += ai_tower.name
                    continue

                ai_bishop = next((a for a in ai_bishoparmies if a.position == (x, 0, z)), None)
                if ai_bishop:
                    line += ai_bishop.name
                    continue

                ai_knight = next((a for a in ai_knightarmies if a.position == (x, 0, z)), None)
                if ai_knight:
                    line += ai_knight.name
                    continue

                ai_queen = next((a for a in ai_queenarmies if a.position == (x, 0, z)), None)
                if ai_queen:
                    line += ai_queen.name
                    continue

                ai_king = next((a for a in ai_kingarmies if a.position == (x, 0, z)), None)
                if ai_king:
                    line += ai_king.name
                    continue

                ai_pawn = next((a for a in aipawnarmies if a.position == (x, 0, z)), None)
                if ai_pawn:
                    line += ai_pawn.name
                    continue

                # Player pieces
                tower = next((t for t in towerarmies if t.position == (x, 0, z)), None)
                if tower:
                    line += tower.name
                    continue

                bishop = next((b for b in bishoparmies if b.position == (x, 0, z)), None)
                if bishop:
                    line += bishop.name
                    continue

                knight = next((k for k in knightarmies if k.position == (x, 0, z)), None)
                if knight:
                    line += knight.name
                    continue

                queen = next((q for q in queenarmies if q.position == (x, 0, z)), None)
                if queen:
                    line += queen.name
                    continue

                king = next((k for k in kingarmies if k.position == (x, 0, z)), None)
                if king:
                    line += king.name
                    continue

                pawn = next((p for p in pawnarmies if p.position == (x, 0, z)), None)
                if pawn:
                    line += pawn.name
                    continue

                # Board tile
                tile = next((t for t in boardmap if t.position == (x, -1, z)), None)
                if tile:
                    line += tile.name
                else:
                    print("error")
                    line = ('')
            print(line)
    if key == 'f5':
        restart_program()
    if key == 'escape':
        exit()        


if __name__ == "__main__":
    main()
