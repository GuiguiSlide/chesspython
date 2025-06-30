from ursina import color, invoke
from classes.piece_base import Piece  # ajuste si ton chemin est différent
towerarmies = []

class Tower(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='T',
            texture='whitemarble',
            model="Tower",
            **kwargs
        )
        self.has_moved = False
        towerarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.color == color.red:
            self.color = color.white
        else :
            self.color = color.red
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
        Tower(position=(0, 0, 0), color=color.white)
        Tower(position=(7, 0, 0), color=color.white)
