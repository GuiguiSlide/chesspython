from ursina import Entity,color,invoke
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
 # Ensure self.color is set after super().__init__
        pawnarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.name=="P":
            for pawns in pawnarmies:
                if pawns.name == "sP":
                    pawns.name = "P"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sP", delay=0.1)

        else:

            self.name = "P"
            print(f'{self.name} unselected')
class Pawnarmy:
    TAILLE = 8  # constante fixe
    def __init__(self):
        for x in range(self.TAILLE):
            pawn = Pawn(position=(x, 0, 1), color=color.orange, name=f'P')  # ex: 'pawn0', 'pawn1', ...
