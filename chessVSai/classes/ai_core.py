import copy

# This function extracts the simplified board state from all armies/entities
def board_state_from_entities():
    # Import armies here to avoid circular import issues
    from classes.ai_tower import ai_towerarmies
    from classes.ai_bishop import ai_bishoparmies
    from classes.ai_knight import ai_knightarmies
    from classes.ai_queen import ai_queenarmies
    from classes.ai_king import ai_kingarmies
    from classes.ai_pawn import aipawnarmies

    from classes.tower import towerarmies
    from classes.bishop import bishoparmies
    from classes.knight import knightarmies
    from classes.queen import queenarmies
    from classes.king import kingarmies
    from classes.pawn import pawnarmies

    state = {}
    # AI pieces
    for p in ai_towerarmies + ai_bishoparmies + ai_knightarmies + ai_queenarmies + ai_kingarmies + aipawnarmies:
        pos = (p.position[0], p.position[2])
        state[pos] = {'type': p.name.lower(), 'color': 'ai'}
    # Player pieces
    for p in towerarmies + bishoparmies + knightarmies + queenarmies + kingarmies + pawnarmies:
        pos = (p.position[0], p.position[2])
        state[pos] = {'type': p.name.lower(), 'color': 'player'}
    return state


class AI_Core:
    def __init__(self, board_state, max_depth=3):
        self.board_state = board_state
        self.max_depth = max_depth

    def evaluate_board(self, board_state):
        piece_values = {
            'p': 1,
            'n': 3,
            'b': 3,
            't': 5,
            'q': 9,
            'k': 1000
        }
        score = 0
        for piece in board_state.values():
            value = piece_values.get(piece['type'], 0)
            if piece['color'] == 'ai':
                score += value
            else:
                score -= value
        return score

    def generate_moves(self, board_state, is_ai_turn):
        moves = []
        for pos, piece in board_state.items():
            if (is_ai_turn and piece['color'] == 'ai') or (not is_ai_turn and piece['color'] == 'player'):
                x, z = pos
                dz = -1 if piece['color'] == 'ai' else 1

                # Forward move
                forward_pos = (x, z + dz)
                if forward_pos not in board_state and 0 <= forward_pos[1] < 8:
                    moves.append((pos, forward_pos))

                # Capture moves (diagonals)
                for dx in [-1, 1]:
                    capture_pos = (x + dx, z + dz)
                    if 0 <= capture_pos[0] < 8 and 0 <= capture_pos[1] < 8:
                        target_piece = board_state.get(capture_pos)
                        if target_piece and target_piece['color'] != piece['color']:
                            moves.append((pos, capture_pos))
        return moves


    def simulate_move(self, board_state, move):
        new_state = copy.deepcopy(board_state)
        from_pos, to_pos = move
        piece = new_state.get(from_pos)
        if piece is None:
            return new_state
        del new_state[from_pos]
        if to_pos in new_state:
            del new_state[to_pos]
        new_state[to_pos] = piece
        return new_state

    def minimax(self, board_state, depth, maximizing_player):
        if depth == 0:
            return self.evaluate_board(board_state), None

        moves = self.generate_moves(board_state, maximizing_player)
        if not moves:
            return self.evaluate_board(board_state), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                new_board = self.simulate_move(board_state, move)
                eval_score, _ = self.minimax(new_board, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                new_board = self.simulate_move(board_state, move)
                eval_score, _ = self.minimax(new_board, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return min_eval, best_move

    def choose_move(self):
        score, best_move = self.minimax(self.board_state, self.max_depth, True)
        return best_move

    def make_move(self):
        move = self.choose_move()
        if move is None:
            print("AI has no valid moves.")
            return

        from_pos, to_pos = move

        # Import AI armies here to find the piece object
        from classes.ai_tower import ai_towerarmies
        from classes.ai_bishop import ai_bishoparmies
        from classes.ai_knight import ai_knightarmies
        from classes.ai_queen import ai_queenarmies
        from classes.ai_king import ai_kingarmies
        from classes.ai_pawn import aipawnarmies

        all_ai_pieces = ai_towerarmies + ai_bishoparmies + ai_knightarmies + ai_queenarmies + ai_kingarmies + aipawnarmies

        piece_obj = None
        for p in all_ai_pieces:
            pos = (p.position[0], p.position[2])  # x, z coords only
            if pos == from_pos:
                piece_obj = p
                break

        if piece_obj is None:
            print(f"Error: no AI piece found at {from_pos}")
            return

        # Update piece position (Ursina vector: x, y, z)
        new_pos_vec = (to_pos[0], piece_obj.position[1], to_pos[1])
        piece_obj.position = new_pos_vec

        print(f"AI moves {piece_obj.name} from {from_pos} to {to_pos}")
