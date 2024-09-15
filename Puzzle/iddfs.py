from solver import Solver
from collections import deque


class IDDFS(Solver):
    def __init__(self, initial_state, max_depth):
        super().__init__(initial_state)
        self.max_frontier_size = 0
        self.max_depth = max_depth

    def dls(self, limit):
        if self.initial_state is None:
            return None

        frontier = deque([(self.initial_state, set())])
        while frontier:
            self.max_frontier_size = max(self.max_frontier_size, len(frontier))
            board, path = frontier.pop()

            if board is None:
                continue

            if board.depth > limit:
                continue

            if board.goal_test():
                return self.set_solution(board)

            board_state = self.get_board_state(board)
            if board_state in path:
                continue

            self.nodes_expanded += 1
            new_path = path | {board_state}

            for neighbor in reversed(board.neighbors()):
                if neighbor is None:
                    continue
                neighbor_state = self.get_board_state(neighbor)
                if neighbor_state not in new_path:
                    frontier.append((neighbor, new_path))

        return None

    def solve(self):
        for depth_limit in range(self.max_depth):
            self.nodes_expanded = 0
            self.max_frontier_size = 0
            solution = self.dls(depth_limit)
            if solution:
                return solution
        return None

    @staticmethod
    def get_board_state(board):
        return tuple(board.state) if board and board.state is not None else None
