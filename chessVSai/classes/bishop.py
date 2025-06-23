from ursina import color, invoke
from classes.piece_base import Piece  # ajuste si ton chemin est différent
bishoparmies = []

class Bishop(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='B',
            **kwargs
        )
        bishoparmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.color == color.red:
            self.color = color.orange
        else :
            self.color = color.red
            if self.name == "B":
                for b in bishoparmies:
                    if b.name == "sB":
                        b.name = "B"
                print(f'{self.name} selected')
                invoke(setattr, self, 'name', "sB", delay=0.1)
            else:
                self.name = "B"
                print(f'{self.name} unselected')

    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position
        directions = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dx, dz in directions:
            nx, nz = x + dx, z + dz
            while 0 <= nx < 8 and 0 <= nz < 8:
                target = board.state[nx][nz]
                if target is None:
                    moves.append((nx, nz))
                elif target.color != self.color:
                    moves.append((nx, nz))
                    break
                else:
                    break
                nx += dx
                nz += dz

        return moves


class Bishoparmy:
    def __init__(self):
        Bishop(position=(2, 0, 0), color=color.orange)
        Bishop(position=(5, 0, 0), color=color.orange)
