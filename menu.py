from ursina import *

def start_multiplayer():
    import subprocess, sys
    subprocess.Popen([sys.executable, 'chessvsmultiplayer/main.py'])
    application.quit()

def start_ai():
    import subprocess, sys
    subprocess.Popen([sys.executable, 'chessvsai/main.py'])
    application.quit()

def quit_game():
    application.quit()

app = Ursina()

window.title = 'Chess Menu'
window.borderless = False
window.size = (1200, 800)
window.fullscreen = True

Text("Chess Menu", y=0.35, scale=2)

Button(text='Play vs Multiplayer', y=0.1, scale=(0.5,0.1), color=color.azure, on_click=start_multiplayer)
Button(text='Play vs AI', y=-0.05, scale=(0.5,0.1), color=color.orange, on_click=start_ai)
Button(text='Quit', y=-0.2, scale=(0.5,0.1), color=color.red, on_click=quit_game)

app.run()