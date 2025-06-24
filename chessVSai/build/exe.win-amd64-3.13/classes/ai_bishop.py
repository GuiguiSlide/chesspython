from ursina import color, Entity
ai_bishoparmies = []
class Ai_Bishop(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="Bishop",
            **kwargs
        )
        ai_bishoparmies.append(self)
    
class Ai_Bishoparmy:
    def __init__(self):
        ai_bishop = Ai_Bishop(position=(2, 0, 7), color=color.black, name=f'B')  # ex: 'pawn0', 'pawn1', ...
        ai_bishop = Ai_Bishop(position=(5, 0, 7), color=color.black, name=f'B')  # ex: 'pawn0', 'pawn1', ...
