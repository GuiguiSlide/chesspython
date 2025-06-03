from ursina import color, Entity
queenarmies = []
class Queen(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        queenarmies.append(self)
    
class Queenarmy:
    def __init__(self):
        queen = Queen(position=(4, 0, 0), color=color.orange, name=f'| Q-A |')  # ex: 'pawn0', 'pawn1', ...  # ex: 'pawn0', 'pawn1', ...
