from ursina import color, Entity
ai_towerarmies = []
class Ai_Tower(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            **kwargs
        )
        ai_towerarmies.append(self)
    
class Ai_Towerarmy:
    def __init__(self):
        ai_tower = Ai_Tower(position=(0, 0, 7), color=color.blue, name=f'T')  # ex: 'pawn0', 'pawn1', ...
        ai_tower = Ai_Tower(position=(7, 0, 7), color=color.blue, name=f'T')  # ex: 'pawn0', 'pawn1', ...
