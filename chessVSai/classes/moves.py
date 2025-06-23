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
        global turn  # Use the global 'turn' variable to switch turns
        if self.onclick:
            self.onclick(self)  # Call the onclick callback if provided

        # Iterate through all piece armies (kings, towers, queens, bishops, knights, pawns)
        for armies in [kingarmies, towerarmies, queenarmies, bishoparmies, knightarmies, pawnarmies]:
            for piece in armies:  # Iterate through each piece in the army
                if hasattr(piece, 'color') and piece.color == color.red:  # Check if the piece is red
                    piece.position = self.position  # Move the piece to the clicked position
                    piece.name = piece.name.replace("s", "")  # Remove 's' from the piece's name
                    piece.color = color.orange  # Change the piece's color to orange
                    handle_captures(1)  # Handle any captures that occur
                    turn = 0  # Set the turn to 0 (likely switching to the other player)
