from ursina import color, Entity
ai_kingarmies = []
class Ai_King(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="King",
            **kwargs
        )
        ai_kingarmies.append(self)
    
class Ai_Kingarmy:
    def __init__(self):
        ai_king = Ai_King(position=(4, 0, 7), color=color.black, name=f'K')  # ex: 'pawn0', 'pawn1', ...
