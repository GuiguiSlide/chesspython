class Rook:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'

    def get_moves(self, board, position):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for dr, dc in directions:
            r, c = position
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = board[r][c]
                    if piece is None:
                        moves.append((r, c))
                    else:
                        if piece.color != self.color:
                            moves.append((r, c))
                        break
                else:
                    break
        return moves