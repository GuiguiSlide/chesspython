from ursina import color, Entity, invoke
kingarmies = []
class King(Entity):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs
        )
        kingarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):

        if self.name=="K":
            for pawns in kingarmies:
                if pawns.name == "sK":
                    pawns.name = "K"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sK", delay=0.1)

        else:

            self.name = "K"
            print(f'{self.name} unselected')
    
class Kingarmy:
    def __init__(self):
        king = King(position=(3, 0, 0), color=color.orange, name=f'K')  # ex: 'pawn0', 'pawn1', ...
