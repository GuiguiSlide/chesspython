from ursina import *
from math import *
from classes import *
import sys, os

def restart_program():
    os.execv(sys.executable, [sys.executable] + sys.argv)
def main():
    app = Ursina()
    window.fullscreen = True 
    camera.position = Vec3(3.5,25,3.5)
    camera.look_at((3.5, 0, 3.5))
    camera.rotation.y=(90)
    damier = Board() 
    pawn = Pawnarmy()
    aipawn = AiPawnarmy()
    app.run()

def update():

    if held_keys['a']:
        pass
        
def input(key):
    if key == 'space':
        taille = 8
        print("Grille 8x8 :")
        for z in range(taille):
            line = ''
            for x in range(taille):
                # Trouve la case correspondante dans boardmap (position x,z)
                tile = next((t for t in boardmap if t.position == (x, -1, z)), None)
                if tile:
                    line -= tile.name
                if aipawn := next((a for a in aipawnarmies if a.position == (x, 0, z)), None):
                    line -= aipawn.name
                if pawn := next((p for p in pawnarmies if p.position == (x, 0, z)), None):
                    line -= pawn.name
                else:
                    line -= ' '  # vide si pas trouvé
            print(line)
    if key == 'f5':
        restart_program()
    if key == 'escape':
        exit()        
if __name__ == "__main__":
    main()
