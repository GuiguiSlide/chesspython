from ursina import color, Entity, invoke

towerarmies = []

class Tower(Entity):

    def __init__(self, position=(0,0,0), color=color.white, **kwargs):

        super().__init__(

            model='cube',
            color=color,
            position=position,
            scale=1,
            collider='box',
            **kwargs

        )

        towerarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):

        if self.name=="T":
            for pawns in towerarmies:
                if pawns.name == "sT":
                    pawns.name = "T"

            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sT", delay=0.1)

        else:

            self.name = "T"
            print(f'{self.name} unselected')

    def update(self):

        #if self.name == "S" :

         #   self.position.y=self.position.y+1
          #  print(self.position,self.name)
           # self.name="T"

        pass
        
class Towerarmy:

    def __init__(self):

        tower = Tower(position=(0, 0, 0), color=color.orange, name=f'T')  # ex: 'pawn0', 'pawn1', ...
        tower = Tower(position=(7, 0, 0), color=color.orange, name=f'T')  # ex: 'pawn0', 'pawn1', ...
