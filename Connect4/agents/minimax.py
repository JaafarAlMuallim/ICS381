import random
import math
from agents.evaluation import Evaluation


class MiniMaxAgent(Evaluation):
    def __init__(self, piece, depth=5):
        super().__init__(piece)
        self.depth = depth
        self.total_score = 0
        self.cumulative_score = 0
        self.pruning_count = 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = super().is_terminal_node(board)

        # If terminal node or depth limit reached, return score
        if depth == 0 or is_terminal:
            if is_terminal:
                # Check if current agent or opponent has won
                if board.winning_move(self.curr_agent_piece):
                    return (None, 100000)  # Extremely high score for win
                elif board.winning_move(self.opponent_piece):
                    return (None, -100000)
                else:
                    return (None, 0)  # No more valid moves, game is over
            else:
                # Depth is zero: return a heuristic evaluation of the board
                return (None, super().score_position(board))

        # Maximizing player (our agent)
        if maximizingPlayer:
            value = -math.inf
            best_column = None

            for col in valid_locations:
                b_copy = board.copy_board()
                b_copy.drop_piece(col, self.curr_agent_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    best_column = col

                alpha = max(alpha, value)
                if alpha >= beta:  # Alpha-beta pruning
                    self.pruning_count += 1
                    break

            if best_column is None:
                best_column = random.choice(valid_locations)  # Random fallback

            return best_column, value

        # Minimizing player (opponent)
        else:
            value = math.inf
            best_column = None

            for col in valid_locations:
                b_copy = board.copy_board()
                b_copy.drop_piece(col, self.opponent_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    best_column = col

                beta = min(beta, value)
                if alpha >= beta:  # Alpha-beta pruning
                    self.pruning_count += 1
                    break

            if best_column is None:
                best_column = random.choice(valid_locations)  # Random fallback

            return best_column, value

    def get_move(self, board):
        col, minimax_score = self.minimax(board, self.depth, -math.inf, math.inf, True)
        self.total_score = minimax_score
        self.cumulative_score += minimax_score  # Accumulate score over game
        return col

    def __str__(self):
        return f"Minimax Agent, Total Score: {self.total_score}, Cumulative Score: {self.cumulative_score}"

    def get_agent(self):
        return "Minimax"

    def get_cumulative_score(self):
        return self.cumulative_score

    def reset_cumulative_score(self):
        self.cumulative_score = 0

    def get_probability(self):
        return "minimax"

    def get_pruning_count(self):
        return self.pruning_count
