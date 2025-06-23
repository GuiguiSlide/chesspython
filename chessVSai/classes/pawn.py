from ursina import Entity, color, invoke
from classes.piece_base import Piece

pawnarmies = []

class Pawn(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='P',
            **kwargs
        )
        pawnarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.color == color.red:
            self.color = color.orange
        else :
            self.color = color.red
            if self.name == "P":
                for p in pawnarmies:
                    if p.name == "sP":
                        p.name = "P"
                print(f'{self.name} selected')
                invoke(setattr, self, 'name', "sP", delay=0.1)
            else:
                self.name = "P"
                print(f'{self.name} unselected')

    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position

        direction = 1 if self.color == color.orange else -1
        # move forward 1
        nx, nz = x, z + direction
        if 0 <= nx < 8 and 0 <= nz < 8 and board.state[nx][nz] is None:
            moves.append((nx, nz))
        # capture diagonally
        for dx in [-1, 1]:
            nx, nz = x + dx, z + direction
            if 0 <= nx < 8 and 0 <= nz < 8:
                target = board.state[nx][nz]
                if target and target.color != self.color:
                    moves.append((nx, nz))
        return moves

class Pawnarmy:
    TAILLE = 8
    def __init__(self):
        for x in range(self.TAILLE):
            Pawn(position=(x, 0, 1), color=color.orange)
