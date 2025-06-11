from ursina import color, Entity, invoke
knightarmies = []
class Knight(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        knightarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):

        if self.name=="C":
            for pawns in knightarmies:
                if pawns.name == "sC":
                    pawns.name = "C"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sC", delay=0.1)

        else:

            self.name = "C"
            print(f'{self.name} unselected')
    
class Knightarmy:
    def __init__(self):
        knight = Knight(position=(1, 0, 0), color=color.orange, name=f'C')  # ex: 'pawn0', 'pawn1', ...
        knight = Knight(position=(6, 0, 0), color=color.orange, name=f'C')  # ex: 'pawn0', 'pawn1', ...
