from ursina import color, Entity
knightarmies = []
class Knight(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        knightarmies.append(self)
    
class Knightarmy:
    def __init__(self):
        knight = Knight(position=(1, 0, 0), color=color.orange, name=f'| C-A |')  # ex: 'pawn0', 'pawn1', ...
        knight = Knight(position=(6, 0, 0), color=color.orange, name=f'| C-A |')  # ex: 'pawn0', 'pawn1', ...
