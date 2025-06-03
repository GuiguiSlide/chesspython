from ursina import color, Entity
bishoparmies = []
class Bishop(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        bishoparmies.append(self)
    
class Bishoparmy:
    def __init__(self):
        bishop = Bishop(position=(2, 0, 0), color=color.orange, name=f'| B-A |')  # ex: 'pawn0', 'pawn1', ...
        bishop = Bishop(position=(5, 0, 0), color=color.orange, name=f'| B-A |')  # ex: 'pawn0', 'pawn1', ...
