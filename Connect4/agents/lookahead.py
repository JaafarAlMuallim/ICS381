import random


class LookAheadAgent:
    def __init__(self, bot_piece):
        self.curr_agent_piece = bot_piece
        if self.curr_agent_piece == 1:
            self.opponent_piece = 2
        else:
            self.opponent_piece = 1

    def get_move(self, board):
        valid_moves = board.get_valid_locations()

        win_move_set = set()
        fallback_move_set = set()
        stop_loss_move_set = set()

        for move in valid_moves:
            bot_copy = board.copy_board()
            player_copy = board.copy_board()

            bot_copy.drop_piece(move, self.curr_agent_piece)
            if bot_copy.winning_move(self.curr_agent_piece):
                win_move_set.add(move)

            player_copy.drop_piece(move, self.opponent_piece)
            if player_copy.winning_move(self.opponent_piece):
                stop_loss_move_set.add(move)
            else:
                fallback_move_set.add(move)

        if len(win_move_set) > 0:
            ret_move = random.choice(list(win_move_set))
        elif len(stop_loss_move_set) > 0:
            ret_move = random.choice(list(stop_loss_move_set))
        elif len(fallback_move_set) > 0:
            ret_move = random.choice(list(fallback_move_set))
        else:
            ret_move = random.choice(valid_moves)

        return ret_move
