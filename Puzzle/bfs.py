from collections import deque
from solver import Solver
from board import Board


class BFS(Solver):
    def __init__(self, initial_state, max_depth):
        super().__init__(initial_state)
        self.frontier = deque()
        self.max_frontier_size = 0
        self.explored_states = set()
        self.max_depth = max_depth

    def solve(self):
        if self.initial_state is None:
            raise ValueError("Initial state cannot be None")

        self.frontier.append(self.initial_state)
        self.explored_states.add(tuple(self.initial_state.state))

        while self.frontier:
            self.max_frontier_size = max(self.max_frontier_size, len(self.frontier))
            board = self.frontier.popleft()
            self.nodes_expanded += 1

            if board.depth > self.max_depth:
                continue

            if board.goal_test():
                self.set_solution(board)
                return

            for neighbor in board.neighbors():
                neighbor_state = tuple(neighbor.state)
                if (
                    neighbor_state not in self.explored_states
                    and neighbor_state not in self.frontier
                ):
                    if neighbor.depth <= self.max_depth:
                        self.frontier.append(neighbor)
                        self.explored_states.add(neighbor_state)
                    else:
                        print("Max depth reached")
        print("No solution found")
        return

    def set_solution(self, board: Board):
        self.solution = board
        return self.solution
