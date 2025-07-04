from ursina import color, Entity
aipawnarmies = []
class Ai_Pawn(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            color=color,
            position=position,
            scale=(0.5, 1, 0.5),
            texture='blackmarble',
            model="Pawn",
            **kwargs
        )
        aipawnarmies.append(self)
    
class Ai_Pawnarmy:
    TAILLE = 8  # constante fixe
    def __init__(self):
        for x in range(self.TAILLE):
            ai_pawn = Ai_Pawn(position=(x, 0, 6), color=color.black, name=f'P')  # ex: 'pawn0', 'pawn1', ...