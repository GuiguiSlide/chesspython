from ursina import color, Entity
towerarmies = []
class Tower(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        towerarmies.append(self)
    
class Towerarmy:
    def __init__(self):
        tower = Tower(position=(0, 0, 0), color=color.orange, name=f'| T-A |')  # ex: 'pawn0', 'pawn1', ...
        tower = Tower(position=(7, 0, 0), color=color.orange, name=f'| T-A |')  # ex: 'pawn0', 'pawn1', ...
