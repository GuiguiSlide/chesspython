from ursina import color, Entity
ai_knightarmies = []
class Ai_Knight(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="Knight",
            **kwargs
        )
        ai_knightarmies.append(self)
    
class Ai_Knightarmy:
    def __init__(self):
        ai_knight = Ai_Knight(position=(1, 0, 7), color=color.white, name=f'C')  # ex: 'pawn0', 'pawn1', ...
        ai_knight = Ai_Knight(position=(6, 0, 7), color=color.white, name=f'C')  # ex: 'pawn0', 'pawn1', ...
