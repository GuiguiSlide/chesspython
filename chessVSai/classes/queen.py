from ursina import color, Entity, invoke
queenarmies = []
class Queen(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        queenarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):

        if self.name=="Q":
            for pawns in queenarmies:
                if pawns.name == "sQ":
                    pawns.name = "Q"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sQ", delay=0.1)

        else:

            self.name = "Q"
            print(f'{self.name} unselected')
    
class Queenarmy:
    def __init__(self):
        queen = Queen(position=(4, 0, 0), color=color.orange, name=f'Q')  # ex: 'pawn0', 'pawn1', ...  # ex: 'pawn0', 'pawn1', ...
