from ursina import color, Entity
kingarmies = []
class King(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        kingarmies.append(self)
    
class Kingarmy:
    def __init__(self):
        king = King(position=(3, 0, 0), color=color.orange, name=f'| K-A |')  # ex: 'pawn0', 'pawn1', ...
