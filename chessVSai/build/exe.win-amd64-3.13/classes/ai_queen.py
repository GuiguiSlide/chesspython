from ursina import color, Entity
ai_queenarmies = []
class Ai_Queen(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="Queen",
            **kwargs
        )
        ai_queenarmies.append(self)
    
class Ai_Queenarmy:
    def __init__(self):
        ai_queen = Ai_Queen(position=(3, 0, 7), color=color.black, name=f'Q')  # ex: 'pawn0', 'pawn1', ...  # ex: 'pawn0', 'pawn1', ...
