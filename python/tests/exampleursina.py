from ursina import *#importe la librairie ursina

app = Ursina()#mets la librairie dans une variable

player = Entity(model='cube', color=color.orange, scale_y=2)#crée une entité en forme de cube orange avec une échelle de 2 sur l'axe y et la mets dans une variable player

def update():
    # time.dt is the time (in seconds) since the last frame; using it ensures smooth, frame-rate independent movement
    player.x += held_keys['d'] * time.dt #position du joueur sur l'axe x + (le temps écoulé * la touche d est enfoncée)
    player.x -= held_keys['a'] * time.dt #position du joueur sur l'axe x - (le temps écoulé * la touche a est enfoncée)
    player.y += held_keys['w'] * time.dt #position du joueur sur l'axe y + (le temps écoulé * la touche w est enfoncée)
    player.y -= held_keys['s'] * time.dt #position du joueur sur l'axe y - (le temps écoulé * la touche s est enfoncée)

def input(key):
    if key == 'space':#si on appuie sur la barre d'espace
        player.y += 1#augmente la position du joueur sur l'axe y de 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)#remet la position du joueur sur l'axe y à sa position initiale après un delais
app.run()#lance l'application