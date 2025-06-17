from ursina import * 
class Move(Entity):
    def __init__(self, *args, onclick=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.onclick = onclick

    def on_click(self):
        if self.onclick:
            self.onclick(self)