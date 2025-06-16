from ursina import color, Entity,invoke
bishoparmies = []
class Bishop(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        bishoparmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        self.color = color.red
        if self.name=="B":
            for pawns in bishoparmies:
                if pawns.name == "sB":
                    pawns.name = "B"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sB", delay=0.1)

        else:

            self.name = "B"
            print(f'{self.name} unselected')
    
class Bishoparmy:
    def __init__(self):
        bishop = Bishop(position=(2, 0, 0), color=color.orange, name=f'B')  # ex: 'pawn0', 'pawn1', ...
        bishop = Bishop(position=(5, 0, 0), color=color.orange, name=f'B')  # ex: 'pawn0', 'pawn1', ...
