from ursina import color, Entity
pawnarmies = []
class Pawn(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        pawnarmies.append(self)
    
class Pawnarmy:
    TAILLE = 8  # constante fixe
    def __init__(self):
        for x in range(self.TAILLE):
            pawn = Pawn(position=(x, 0, 1), color=color.orange, name=f'|P-A-{x}|')  # ex: 'pawn0', 'pawn1', ...