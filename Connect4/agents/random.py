import random
from agents.evaluation import Evaluation


class RandomAgent(Evaluation):
    def __init__(self, piece, depth=3):
        super().__init__(piece)
        self.bot_piece = piece
        self.depth = depth
        self.cumulative_score = 0

    def random(self, board, depth, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.winning_move(self.curr_agent_piece):
                    return (None, 100000)
                elif board.winning_move(self.opponent_piece):
                    return (None, -100000)
                else:  # Game is over, it's a draw
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board))

        # Choose a random move
        column = random.choice(valid_locations)
        b_copy = board.copy_board()

        if maximizingPlayer:
            b_copy.drop_piece(column, self.curr_agent_piece)
            _, score = self.random(b_copy, depth - 1, False)
        else:
            b_copy.drop_piece(column, self.opponent_piece)
            _, score = self.random(b_copy, depth - 1, True)

        return column, score

    def get_move(self, board):
        col, random_score = self.random(board, self.depth, True)
        self.cumulative_score += random_score
        return col

    def __str__(self):
        return "Random Agent"

    def get_agent(self):
        return "Random"

    def get_cumulative_score(self):
        return self.cumulative_score

    def reset_cumulative_score(self):
        self.cumulative_score = 0

    def get_probability(self):
        return "random"

    def get_pruning_count(self):
        return 0
