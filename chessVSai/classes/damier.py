from ursina import color, Entity
boardmap=[]
class BoardTile(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        boardmap.append(self)
    def on_click(self):
        print(f"Case cliquée à {self.position}")

class Board:
    TAILLE = 8  # constante fixe

    def __init__(self):
        self.tiles = []
        for x in range(self.TAILLE):
            for z in range(self.TAILLE):
                color_case = color.white if (x + z) % 2 == 0 else color.black
                letter = chr(ord('a') + x)  # 'a' + x
                number = str(z + 1)         # 1-based index pour les lignes
                tile_name = f'{letter}{number}'  # ex: 'a1', 'b5'
                tile = BoardTile(position=(x, 0, z), color=color_case, name=tile_name)
                self.tiles.append(tile)


