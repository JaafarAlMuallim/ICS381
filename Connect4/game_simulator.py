import pandas as pd
import numpy as np
from board import Board
import time
from typing import List, Tuple


class GameSimulator:
    def __init__(self):
        self.data = []

    def run_game(self, p1, p2) -> Tuple[Board, int, int]:
        turn = Board.PLAYER1_PIECE
        board = Board(turn)
        # board.print_board()

        time_p1 = time_p2 = moves_count_p1 = moves_count_p2 = 0
        game_over = False

        while not game_over:
            current_player = p1 if turn == Board.PLAYER1_PIECE else p2
            start = time.perf_counter()
            col = current_player.get_move(board)

            if board.is_valid_location(col):
                board.drop_piece(col, turn)
                if turn == Board.PLAYER1_PIECE:
                    moves_count_p1 += 1
                    time_p1 += time.perf_counter() - start
                else:
                    moves_count_p2 += 1
                    time_p2 += time.perf_counter() - start

                game_over = self.check_win(board, turn)
                if not game_over:
                    turn = self.next_turn(board, turn)

        # self._print_game_results(
        #     p1, p2, time_p1, time_p2, moves_count_p1, moves_count_p2, board
        # )
        return board, moves_count_p1, moves_count_p2

    def next_turn(self, board, turn):
        # print(f"\nPlayer {turn}'s Turn\n")
        # board.print_board()
        return (
            Board.PLAYER2_PIECE if turn == Board.PLAYER1_PIECE else Board.PLAYER1_PIECE
        )

    def check_win(self, board, piece):
        if board.winning_move(piece):
            print(f"\nPLAYER {piece} WINS!\n")
            return True
        if board.check_draw():
            print("\nIT'S A TIE!\n")
            return True
        return False

    def _print_game_results(
        self, p1, p2, time_p1, time_p2, moves_count_p1, moves_count_p2, board
    ):
        print(board)
        print(f"\nAgent 1 [{p1}]")
        print(f"TIME: {time_p1:.2f} seconds")
        print(f"MOVES: {moves_count_p1}")
        print(f"\nAgent 2 [{p2}]")
        print(f"TIME: {time_p2:.2f} seconds")
        print(f"MOVES: {moves_count_p2}")

    def run_set(self, p1, p2, num_games=10, set_name="set1") -> List[dict]:
        moves_p1_list, moves_p2_list, p1_list, p2_list = [], [], [], []

        for _ in range(num_games):
            p1.reset_cumulative_score()
            p2.reset_cumulative_score()
            board, moves_p1, moves_p2 = self.run_game(p1, p2)
            p1_list.append(p1)
            p2_list.append(p2)
            moves_p1_list.append(moves_p1)
            moves_p2_list.append(moves_p2)

            self.data.append(self._create_game_data(p1, p2, board))

        stats = self.calculate_game_statistics(
            p1_list, p2_list, moves_p1_list, moves_p2_list, num_games
        )
        pd.DataFrame([stats]).to_excel(f"{set_name}.xlsx")
        return self.data

    def _create_game_data(self, p1, p2, board):
        return {
            "Agent 1": p1.get_agent(),
            "Agent 2": p2.get_agent(),
            "Agent 1 Score": p1.get_cumulative_score(),
            "Agent 2 Score": p2.get_cumulative_score(),
            "Agent 1 Probability": p1.get_probability(),
            "Agent 2 Probability": p2.get_probability(),
            "Winner": (
                f"{p1.get_agent()} {p1.get_probability()}"
                if self.check_win(board, Board.PLAYER1_PIECE)
                else f"{p2.get_agent()} {p2.get_probability()}"
            ),
            "Board": board,
        }

    @staticmethod
    def calculate_game_statistics(p1_list, p2_list, moves_p1, moves_p2, num_games=10):
        wins, losses = {"Agent 1": 0, "Agent 2": 0}, {"Agent 1": 0, "Agent 2": 0}
        game_lengths, pruning_counts = [], []

        for i in range(num_games):
            winner = "Agent 2" if moves_p1[i] == moves_p2[i] else "Agent 1"
            loser = "Agent 2" if winner == "Agent 1" else "Agent 1"
            wins[winner] += 1
            losses[loser] += 1
            game_lengths.append(max(moves_p1[i], moves_p2[i]))
            pruning_counts.append(
                p1_list[i].get_pruning_count() + p2_list[i].get_pruning_count()
            )

        stats = {}
        for agent in ["Agent 1", "Agent 2"]:
            stats[f"{agent} Win-to-Loss Ratio"] = (
                wins[agent] / losses[agent]
                if losses[agent] > 0
                else (float("1") if wins[agent] > 0 else 0)
            )

        stats.update(
            {
                "Min Game Length": min(game_lengths),
                "Max Game Length": max(game_lengths),
                "Average Game Length": np.mean(game_lengths),
                "Std Dev Game Length": np.std(game_lengths),
                "Min Pruning Count": min(pruning_counts),
                "Max Pruning Count": max(pruning_counts),
                "Average Pruning Count": np.mean(pruning_counts),
                "Std Dev Pruning Count": np.std(pruning_counts),
            }
        )

        return stats
