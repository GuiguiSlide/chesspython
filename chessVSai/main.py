from ursina import *
from math import *
from classes import *

import sys, os
import time

playerarmy = [towerarmies, queenarmies, knightarmies, pawnarmies, kingarmies, bishoparmies]
aiarmy = [ai_bishoparmies, ai_kingarmies, aipawnarmies, ai_queenarmies, ai_towerarmies, ai_knightarmies]
alltowers = [aiarmy, playerarmy]

def main():

    app = Ursina()
    window.fullscreen = False 
    
    camera.position = Vec3(3.5,60,3.5)
    camera.look_at((3.5, 0, 3.5))
    camera.rotation.y=(90)
    
    damier = Board() 
    
    pawn = Pawnarmy()
    knight = Knightarmy()
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
    
    playerarmy = [tower,queen,knight,pawn,king,bishop]
    aiarmy = [ai_bishop,ai_king,ai_pawn,ai_queen,ai_tower,ai_knight]
    
    app.run()

def update():
    moves()
    if not hasattr(update, "last_print_time"):
        update.last_print_time = time.time()
    current_time = time.time()
    if current_time - update.last_print_time >= 8:
        taille = 8
        print("Grille 8x8 :")
        for z in range(taille, -1, -1):
            line = ''
            for x in range(taille):
                # AI pieces
                ai_tower = next((a for a in ai_towerarmies if a.position == (x, 0, z)), None)
                if ai_tower:
                    line += ai_tower.name + "    "
                    continue

                ai_bishop = next((a for a in ai_bishoparmies if a.position == (x, 0, z)), None)
                if ai_bishop:
                    line += ai_bishop.name + "    "
                    continue

                ai_knight = next((a for a in ai_knightarmies if a.position == (x, 0, z)), None)
                if ai_knight:
                    line += ai_knight.name + "    "
                    continue

                ai_queen = next((a for a in ai_queenarmies if a.position == (x, 0, z)), None)
                if ai_queen:
                    line += ai_queen.name + "    "
                    continue

                ai_king = next((a for a in ai_kingarmies if a.position == (x, 0, z)), None)
                if ai_king:
                    line += ai_king.name + "    "
                    continue

                ai_pawn = next((a for a in aipawnarmies if a.position == (x, 0, z)), None)
                if ai_pawn:
                    line += ai_pawn.name + "    "
                    continue

                # Player pieces
                tower = next((t for t in towerarmies if t.position == (x, 0, z)), None)
                if tower:
                    line += tower.name + "    "
                    continue

                bishop = next((b for b in bishoparmies if b.position == (x, 0, z)), None)
                if bishop:
                    line += bishop.name + "    "
                    continue

                knight = next((k for k in knightarmies if k.position == (x, 0, z)), None)
                if knight:
                    line += knight.name + "    "
                    continue

                queen = next((q for q in queenarmies if q.position == (x, 0, z)), None)
                if queen:
                    line += queen.name + "    "
                    continue

                king = next((k for k in kingarmies if k.position == (x, 0, z)), None)
                if king:
                    line += king.name + "    "
                    continue

                pawn = next((p for p in pawnarmies if p.position == (x, 0, z)), None)
                if pawn:
                    line += pawn.name + "    "
                    continue

                # Board tile
                tile = next((t for t in boardmap if t.position == (x, -1, z)), None)
                if tile:
                    line += tile.name + "  "
                else:
                    line = ('')
            print(line)
        update.last_print_time = current_time
        
def input(key):

    if key == 'f':
        if window.fullscreen == False:
            window.fullscreen = True
        else:
            window.fullscreen = False

    if key == 'f5':
        restart_program()

    if key == 'escape':
        exit()     

    if key == 'b':
        #debug
        #checks inside the list alltowers witch are group allies and enemies
        for all in alltowers:
            #check inside the lists inside the list alltowers inside aiarmies or playerarmies ex: ponarmies  
            for alles in all:
                #check ex: inside ponarmies
                for xall in alles:
                    # print the towers 
                    print(xall.name)
                    #check if selected tower contain s fro selected in its name
                    if "s" in xall.name:
                        #move selected tower foward
                        xall.position = Vec3(xall.position.x, xall.position.y, xall.position.z+1)
                        #modify the name of the selected tower to unselect itself
                        xall.name = xall.name.replace("s", "")
                        
def restart_program():

    os.execv(sys.executable, [sys.executable] + sys.argv)

def moves():
    #checks inside the list alltowers witch are group allies and enemies
    for all in alltowers:
        #check inside the lists inside the list alltowers inside aiarmies or playerarmies ex: ponarmies  
        for alles in all:
            #check ex: inside ponarmies
            for xall in alles:
                if xall.color == color.red:
                    if xall.name == "sT":
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x, xall.position.y, xall.position.z + 1),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)
                    if xall.name == "sQ":
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x, xall.position.y, xall.position.z + 1),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)
                    if xall.name == "sK":
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x, xall.position.y, xall.position.z + 1),
                            scale=1
                        )
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x, xall.position.y, xall.position.z - 1),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)
                    if xall.name == "sP":
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x, xall.position.y, xall.position.z + 1),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)
                    if xall.name == "sC":   
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x - 1, xall.position.y, xall.position.z + 2),
                            scale=1
                        )                     
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x + 1, xall.position.y, xall.position.z + 2),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)
                    if xall.name == "sB":
                        possiblemoves = Entity(
                            model='cube',
                            color=color.green,
                            position=Vec3(xall.position.x + 1, xall.position.y, xall.position.z + 1),
                            scale=1
                        )
                        destroy(possiblemoves, delay=0.2)

if __name__ == "__main__":
    main()
