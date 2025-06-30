from ursina import color, Entity, invoke
from classes.piece_base import Piece  # Assure-toi que ce chemin est correct
kingarmies = []

class King(Piece):
    def __init__(self, position=(0,0,0), color=color.white, **kwargs):
        super().__init__(
            position=position,
            color=color,
            name='K',
            texture='whitemarble',
            model="King",
            **kwargs
        )
        self.has_moved = False
        kingarmies.append(self)
        self.on_click = self.on_click_event

    def on_click_event(self):
        if self.color == color.red:
            self.color = color.white
        else:
            self.color = color.red

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

        # Roque (Castling) logic
        if not self.has_moved:
            row = x
            # Kingside castling
            if self._can_castle(board, kingside=True):
                moves.append((x, z + 2))
            # Queenside castling
            if self._can_castle(board, kingside=False):
                moves.append((x, z - 2))
        return moves

    def _can_castle(self, board, kingside=True):
        x, z = self.board_position
        row = x
        if kingside:
            rook_z = 7
            step = 1
            spaces = [z + 1, z + 2]
        else:
            rook_z = 0
            step = -1
            spaces = [z - 1, z - 2, z - 3]

        # Check rook presence and has_moved
        rook = board.state[row][rook_z]
        if not rook or getattr(rook, 'name', None) != 'R' or getattr(rook, 'has_moved', True):
            return False

        # Check spaces between king and rook are empty
        for nz in range(min(z, rook_z) + 1, max(z, rook_z)):
            if board.state[row][nz] is not None:
                return False

        # Optionally: Check king is not in check, and does not pass through check
        # This requires board.is_in_check(color) and board.simulate_move()
        # For simplicity, omitted here

        return True

class Kingarmy:
    def __init__(self):
        King(position=(3, 0, 0), color=color.white)
