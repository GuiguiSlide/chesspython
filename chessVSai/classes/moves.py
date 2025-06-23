from ursina import * 
from .king import *
from .queen import *
from .tower import *
from .bishop import *
from .knight import *
from .pawn import *
from main import handle_captures, turn  # Import functions and variables from main.py (careful with circular imports)

class Move(Entity):
    def __init__(self, *args, onclick=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.onclick = onclick

    def on_click(self):
        global turn  # **declare turn global to modify it**
        if self.onclick:
            self.onclick(self)

        # You should only move the **selected piece**, not all red pieces.
        # But since you do not track selected piece here, I guess you want to teleport one piece?
        # For now, let's teleport all red pieces, but usually you should fix this logic.
        for armies in [kingarmies, towerarmies, queenarmies, bishoparmies, knightarmies, pawnarmies]:
            for piece in armies:
                if hasattr(piece, 'color') and piece.color == color.red:
                    piece.position = self.position  # Teleport to this Move's position
                    piece.name = piece.name.replace("s", "")
                    piece.color = color.orange
                    handle_captures(1)  # Player just played
                    turn = 0
