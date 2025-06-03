from ursina import color, Entity
aipawnarmies = []
class AiPawn(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        aipawnarmies.append(self)
    
class AiPawnarmy:
    TAILLE = 8  # constante fixe
    def __init__(self):
        for x in range(self.TAILLE):
            aipawn = AiPawn(position=(x, 0, 6), color=color.blue, name=f'|P-E-{x}|')  # ex: 'pawn0', 'pawn1', ...