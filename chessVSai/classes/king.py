from ursina import color, Entity, invoke
from classes.piece_base import Piece  # Assure-toi que ce chemin est correct
kingarmies = []

class King(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='K',
            **kwargs
        )
        kingarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.color == color.red:
            self.color = color.orange
        else :
            self.color = color.red
            if self.name == "K":
                for king in kingarmies:
                    if king.name == "sK":
                        king.name = "K"
                print(f'{self.name} selected')
                invoke(setattr, self, 'name', "sK", delay=0.1)
            else:
                self.name = "K"
                print(f'{self.name} unselected')

    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position

        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Up, Down, Right, Left
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
        ]

        for dx, dz in directions:
            nx, nz = x + dx, z + dz
            if 0 <= nx < 8 and 0 <= nz < 8:
                target = board.state[nx][nz]
                if target is None or target.color != self.color:
                    moves.append((nx, nz))
        return moves

class Kingarmy:
    def __init__(self):
        King(position=(3, 0, 0), color=color.orange)
