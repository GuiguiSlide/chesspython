from ursina import *
def main():
    app = Ursina()
    cube = Entity(model='cube', color=color.azure, scale=(2,2,2), position=(0,0,0))
    app.run()

if __name__ == "__main__":
    main()