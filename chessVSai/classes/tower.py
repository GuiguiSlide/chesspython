from ursina import color, invoke
from classes.piece_base import Piece  # ajuste si ton chemin est différent
towerarmies = []

class Tower(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='T',
            **kwargs
        )
        towerarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        self.color = color.red
        if self.name == "T":
            for t in towerarmies:
                if t.name == "sT":
                    t.name = "T"
                    t.color = color.orange  # Reset color
            print(f'{self.name} selected')
            invoke(setattr, self, 'name', "sT", delay=0.1)
        else:
            self.name = "T"
            print(f'{self.name} unselected')

    def get_legal_moves(self, board):
        moves = []
        x, z = self.board_position

        # 4 directions : haut, bas, gauche, droite
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

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


class Towerarmy:
    def __init__(self):
        Tower(position=(0, 0, 0), color=color.orange)
        Tower(position=(7, 0, 0), color=color.orange)
