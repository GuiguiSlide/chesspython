from ursina import color, Entity
ai_towerarmies = []
class Ai_Tower(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="Tower",
            **kwargs
        )
        ai_towerarmies.append(self)
    
class Ai_Towerarmy:
    def __init__(self):
        ai_tower = Ai_Tower(position=(0, 0, 7), color=color.black, name=f'T')  # ex: 'pawn0', 'pawn1', ...
        ai_tower = Ai_Tower(position=(7, 0, 7), color=color.black, name=f'T')  # ex: 'pawn0', 'pawn1', ...
