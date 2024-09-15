import random
import math
from agents.evaluation import Evaluation


class ExpectiMaxAgent(Evaluation):
    def __init__(self, piece, probability=0.75, depth=5):
        super().__init__(piece)
        self.depth = depth
        self.probability = probability
        self.total_score = 0
        self.cumulative_score = 0
        self.pruning_count = 0

    def expectimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = super().is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(self.curr_agent_piece):
                    return (None, 100000, [])
                elif board.winning_move(self.opponent_piece):
                    return (None, -100000, [])
                else:
                    return (None, 0, [])
            else:
                return (None, super().score_position(board), [])

        if maximizingPlayer:
            best_score = -math.inf
            best_column = valid_locations[0]  # Ensure we initialize with a valid column
            move_scores = []

            for col in valid_locations:
                b_copy = board.copy_board()
                b_copy.drop_piece(col, self.curr_agent_piece)
                score = self.expectimax(b_copy, depth - 1, alpha, beta, False)[1]
                move_scores.append((col, score))

                # Update alpha and check for pruning
                alpha = max(alpha, score)
                if alpha >= beta:
                    self.pruning_count += 1
                    break  # Break out if pruning occurs

                # Track the best score and best column
                if score > best_score:
                    best_score = score
                    best_column = col

            return best_column, best_score, move_scores
        else:
            # Expectimax logic for minimizing player (MiniMax logic with alpha-beta pruning)
            total_score = 0
            move_scores = []
            num_valid_moves = len(valid_locations)

            for col in valid_locations:
                b_copy = board.copy_board()
                b_copy.drop_piece(col, self.opponent_piece)
                score = self.expectimax(b_copy, depth - 1, alpha, beta, True)[1]
                total_score += score
                move_scores.append((col, score))

            expected_value = total_score / num_valid_moves if num_valid_moves > 0 else 0
            return random.choice(valid_locations), expected_value, move_scores

    def get_move(self, board):
        best_col, best_score, move_scores = self.expectimax(
            board, self.depth, -math.inf, math.inf, True
        )

        reasonable_moves = [
            (col, score) for col, score in move_scores if score > 0 and col != best_col
        ]

        if random.random() < self.probability:
            self.total_score = best_score
            self.cumulative_score += best_score
            return best_col
        else:
            # With probability 1-p, choose a reasonable (but not random) suboptimal move
            if reasonable_moves:
                random_choice = random.choice(reasonable_moves)
                col, score = random_choice  # random_choice is a tuple (col, score)
                self.total_score = score
                self.cumulative_score += score
                return col
            else:
                # Fallback to the best move if no reasonable alternatives are found
                self.total_score = best_score
                self.cumulative_score += best_score
                return best_col

    def __str__(self):
        return (
            f"Expectimax Agent, Total Score: {self.total_score}, "
            f"Cumulative Score: {self.cumulative_score}, Probability: {self.probability}"
        )

    def get_agent(self):
        return "Expectimax"

    def get_cumulative_score(self):
        return self.cumulative_score

    def reset_cumulative_score(self):
        self.cumulative_score = 0

    def get_probability(self):
        return self.probability

    def get_pruning_count(self):
        return self.pruning_count
