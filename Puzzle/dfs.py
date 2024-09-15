from solver import Solver
from collections import deque


class DFS(Solver):
    def __init__(self, initial_state, max_depth=80):
        super().__init__(initial_state)
        self.frontier = deque()
        self.explored_nodes = {}
        self.max_depth = max_depth
        self.curr_depth = 0
        self.max_frontier_size = 0

    def solve(self):
        self.frontier.append(self.initial_state)
        while self.frontier:
            self.max_frontier_size = max(self.max_frontier_size, len(self.frontier))
            board = self.frontier.pop()

            print(board.depth)
            if board.depth > self.max_depth:
                continue  # Skip this state and continue with the next one in the frontier

            if board.goal_test():
                self.set_solution(board)
                return

            board_state = tuple(board.state)
            if (
                board_state in self.explored_nodes
                and self.explored_nodes[board_state] <= board.depth
            ):
                continue

            self.explored_nodes[board_state] = board.depth
            self.nodes_expanded += 1

            neighbors = board.neighbors()
            for neighbor in reversed(neighbors):
                self.frontier.append(neighbor)

        print("No solution found")
        return
