from ursina import color, invoke
from classes.piece_base import Piece  # ajuste si besoin
queenarmies = []

class Queen(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='Q',
            **kwargs
        )
        queenarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        self.color = color.red
        if self.name == "Q":
            for q in queenarmies:
                if q.name == "sQ":
                    q.name = "Q"
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sQ", delay=0.1)
        else:
            self.name = "Q"
            print(f'{self.name} unselected')

    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position

        # 8 directions : tour + fou
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # vertical/horizontal (tour)
            (1, 1), (-1, -1), (-1, 1), (1, -1)  # diagonales (fou)
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


class Queenarmy:
    def __init__(self):
        Queen(position=(4, 0, 0), color=color.orange)
