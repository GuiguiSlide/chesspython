import copy
import random
from collections import defaultdict

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
    def __init__(self, board_state, max_depth=10):  # Set max_depth to 2 for 2 moves ahead
        self.board_state = board_state
        self.max_depth = max_depth
        self.previous_moves = []
        
    def evaluate_board(self, board_state):
        piece_values = {
            'p': 10,
            'n': 35,
            'b': 30,
            't': 50,
            'q': 90,
            'k': 10000
        }
        
        score = 0
        ai_pieces = 0
        player_pieces = 0
        
        for pos, piece in board_state.items():
            x, z = pos
            value = piece_values.get(piece['type'], 0)
            
            # Material evaluation
            if piece['color'] == 'ai':
                score += value
                ai_pieces += 1
                
                # Pawn promotion bonus
                if piece['type'] == 'p' and z == 0:
                    score += 80
                    
                # Center control bonus for pawns
                if piece['type'] == 'p' and 3 <= x <= 4 and 2 <= z <= 5:
                    score += 5
                    
            else:
                score -= value
                player_pieces += 1
                
                # Pawn promotion bonus for player
                if piece['type'] == 'p' and z == 7:
                    score -= 80
                    
                # Center control penalty for player pawns
                if piece['type'] == 'p' and 3 <= x <= 4 and 2 <= z <= 5:
                    score -= 5
        
        # King safety - encourage castling by penalizing center king in early game
        ai_king_pos = None
        player_king_pos = None
        
        for pos, piece in board_state.items():
            if piece['type'] == 'k':
                if piece['color'] == 'ai':
                    ai_king_pos = pos
                else:
                    player_king_pos = pos
        
        if ai_king_pos and (ai_pieces + player_pieces) > 20:  # Early/mid game
            x, z = ai_king_pos
            if 3 <= x <= 4:  # King in center files
                score -= 20
                
        if player_king_pos and (ai_pieces + player_pieces) > 20:
            x, z = player_king_pos
            if 3 <= x <= 4:
                score += 20
        
        return score

    def generate_moves(self, board_state, is_ai_turn):
        moves = []
        capture_moves = []
        quiet_moves = []

        for pos, piece in board_state.items():
            if (is_ai_turn and piece['color'] == 'ai') or (not is_ai_turn and piece['color'] == 'player'):
                x, z = pos
                piece_type = piece['type']
                color = piece['color']
                dz = -1 if color == 'ai' else 1  # Forward direction

                if piece_type == 'p':  # Pawn
                    # Forward move
                    forward_pos = (x, z + dz)
                    if forward_pos not in board_state and 0 <= forward_pos[1] < 8:
                        quiet_moves.append((pos, forward_pos))
                    
                    # Double forward move from starting position
                    if (color == 'ai' and z == 6) or (color == 'player' and z == 1):
                        double_forward_pos = (x, z + 2*dz)
                        if forward_pos not in board_state and double_forward_pos not in board_state:
                            quiet_moves.append((pos, double_forward_pos))
                    
                    # Captures
                    for dx in [-1, 1]:
                        capture_pos = (x + dx, z + dz)
                        if 0 <= capture_pos[0] < 8 and 0 <= capture_pos[1] < 8:
                            target = board_state.get(capture_pos)
                            if target and target['color'] != color:
                                capture_moves.append((pos, capture_pos))

                elif piece_type == 'n':  # Knight
                    deltas = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
                    for dx, dz_ in deltas:
                        nx, nz = x + dx, z + dz_
                        if 0 <= nx < 8 and 0 <= nz < 8:
                            target = board_state.get((nx, nz))
                            if not target:
                                quiet_moves.append((pos, (nx, nz)))
                            elif target['color'] != color:
                                capture_moves.append((pos, (nx, nz)))

                elif piece_type == 'b':  # Bishop
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    for dx, dz_ in directions:
                        nx, nz = x + dx, z + dz_
                        while 0 <= nx < 8 and 0 <= nz < 8:
                            target = board_state.get((nx, nz))
                            if not target:
                                quiet_moves.append((pos, (nx, nz)))
                            elif target['color'] != color:
                                capture_moves.append((pos, (nx, nz)))
                                break
                            else:
                                break
                            nx += dx
                            nz += dz_

                elif piece_type == 't':  # Rook (Tower)
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    for dx, dz_ in directions:
                        nx, nz = x + dx, z + dz_
                        while 0 <= nx < 8 and 0 <= nz < 8:
                            target = board_state.get((nx, nz))
                            if not target:
                                quiet_moves.append((pos, (nx, nz)))
                            elif target['color'] != color:
                                capture_moves.append((pos, (nx, nz)))
                                break
                            else:
                                break
                            nx += dx
                            nz += dz_

                elif piece_type == 'q':  # Queen
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
                    for dx, dz_ in directions:
                        nx, nz = x + dx, z + dz_
                        while 0 <= nx < 8 and 0 <= nz < 8:
                            target = board_state.get((nx, nz))
                            if not target:
                                quiet_moves.append((pos, (nx, nz)))
                            elif target['color'] != color:
                                capture_moves.append((pos, (nx, nz)))
                                break
                            else:
                                break
                            nx += dx
                            nz += dz_

                elif piece_type == 'k':  # King
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
                    for dx, dz_ in directions:
                        nx, nz = x + dx, z + dz_
                        if 0 <= nx < 8 and 0 <= nz < 8:
                            target = board_state.get((nx, nz))
                            if not target:
                                quiet_moves.append((pos, (nx, nz)))
                            elif target['color'] != color:
                                capture_moves.append((pos, (nx, nz)))
        
        # Move ordering: captures first, then quiet moves
        moves.extend(capture_moves)
        moves.extend(quiet_moves)
        
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

    def minimax(self, board_state, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(board_state), None

        moves = self.generate_moves(board_state, maximizing_player)
        if not moves:
            return self.evaluate_board(board_state), None

        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = self.simulate_move(board_state, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                
                # Penalize repeating moves
                if move in self.previous_moves[-2:]:  # Last 2 moves
                    eval_score -= 10
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = self.simulate_move(board_state, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                
                # Penalize repeating moves for player
                if move in self.previous_moves[-2:]:
                    eval_score += 10
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def choose_move(self):
        # Start with alpha-beta pruning
        score, best_move = self.minimax(self.board_state, self.max_depth, float('-inf'), float('inf'), True)
        return best_move

    def make_move(self):
        move = self.choose_move()
        if move is None:
            print("AI has no valid moves.")
            return

        # Save the move played
        self.previous_moves.append(move)
        if len(self.previous_moves) > 4:  # Keep only last 4 moves
            self.previous_moves.pop(0)

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
            pos = (p.position[0], p.position[2])
            if pos == from_pos:
                piece_obj = p
                break

        if piece_obj is None:
            print(f"Error: no AI piece found at {from_pos}")
            return

        new_pos_vec = (to_pos[0], piece_obj.position[1], to_pos[1])
        piece_obj.position = new_pos_vec

        print(f"AI moves {piece_obj.name} from {from_pos} to {to_pos}")