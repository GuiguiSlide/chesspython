from ursina import color, Entity
ai_queenarmies = []
class Ai_Queen(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        ai_queenarmies.append(self)
    
class Ai_Queenarmy:
    def __init__(self):
        ai_queen = Ai_Queen(position=(3, 0, 7), color=color.blue, name=f'Q')  # ex: 'pawn0', 'pawn1', ...  # ex: 'pawn0', 'pawn1', ...
