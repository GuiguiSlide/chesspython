from ursina import *
from math import *
from classes import *
import sys, os
def restart_program():
    print("Restarting program...")
    os.execv(sys.executable, [sys.executable] + sys.argv)
def main():
    

    
    app = Ursina()
    editor_camera = EditorCamera()
    damier = Board() 
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
                tile = next((t for t in boardmap if t.position == (x, 0, z)), None)
                if tile:
                    line += tile.name
                else:
                    line += ' '  # vide si pas trouvé
            print(line)
    if key == 'f5':
        restart_program()
    if key == 'escape':
        exit()




        
if __name__ == "__main__":
    main()
