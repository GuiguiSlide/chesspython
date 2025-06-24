from ursina import color, invoke
from classes.piece_base import Piece

knightarmies = []

class Knight(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position, 
            color=color, 
            name="C",
            texture='whitemarble',
            model="Knight", 
            **kwargs
            )
        knightarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):

        if self.color == color.red:
            self.color = color.white
        else :
            self.color = color.red


    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position
        offsets = [
            (1, 2), (-1, 2), (2, 1), (-2, 1),
            (1, -2), (-1, -2), (2, -1), (-2, -1),
        ]
        for dx, dz in offsets:
            nx, nz = x + dx, z + dz
            if 0 <= nx < 8 and 0 <= nz < 8:
                target = board.state[nx][nz]
                if target is None or target.color != self.color:
                    moves.append((nx, nz))
        return moves

class Knightarmy:
    def __init__(self):
        Knight(position=(1, 0, 0), color=color.white)
        Knight(position=(6, 0, 0), color=color.white)
