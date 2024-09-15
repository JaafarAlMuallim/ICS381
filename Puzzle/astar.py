import heapq
from solver import Solver


class AStar(Solver):
    def __init__(self, initial_state):
        super(AStar, self).__init__(initial_state)
        self.initial_state = initial_state
        self.frontier = []
        self.explored = {}
        self.max_frontier_size = 0
        self.max_depth = 0
        # Track heuristic costs separately
        self.cost_manhattan = 0
        self.cost_misplaced = 0
        self.cost_euclidean = 0
        self.manhattan_error = 0
        self.misplaced_error = 0
        self.euclidean_error = 0
        self.node_count = 0

    def solve(self):
        heapq.heappush(self.frontier, self.initial_state)

        while self.frontier:
            board = heapq.heappop(self.frontier)
            self.max_frontier_size = max(self.max_frontier_size, len(self.frontier))

            self.cost_manhattan = board.cost_manhattan
            self.cost_misplaced = board.cost_misplaced
            self.cost_euclidean = board.cost_euclidean

            # check if resources usage or time are high

            if board.goal_test():
                self.set_solution(board)
                break

            state_tuple = tuple(board.state)
            if (
                state_tuple not in self.explored
                or board.depth < self.explored[state_tuple]
            ):
                self.explored[state_tuple] = board.depth
                for neighbor in board.neighbors():
                    neighbor_tuple = tuple(neighbor.state)
                    if (
                        neighbor_tuple not in self.explored
                        or neighbor.depth < self.explored[neighbor_tuple]
                    ):
                        heapq.heappush(self.frontier, neighbor)
                        self.max_depth = max(self.max_depth, neighbor.depth)

            # Heuristic comparison
            manhattan_error = abs(board.cost_manhattan - board.depth)
            misplaced_error = abs(board.cost_misplaced - board.depth)
            euclidean_error = abs(board.cost_euclidean - board.depth)

            self.manhattan_error += manhattan_error
            self.misplaced_error += misplaced_error
            self.euclidean_error += euclidean_error
            self.node_count += 1

        return self.solution

    def heuristic_comparison(self):
        avg_manhattan_error = self.manhattan_error / self.node_count
        avg_misplaced_error = self.misplaced_error / self.node_count
        avg_euclidean_error = self.euclidean_error / self.node_count

        return {
            "Manhattan": avg_manhattan_error,
            "Misplaced": avg_misplaced_error,
            "Euclidean": avg_euclidean_error,
        }

    def __str__(self):
        # Display all costs
        return (
            f"Max Frontier Size: {self.max_frontier_size}\n"
            f"Max Depth: {self.max_depth}\n"
            f"Path to Goal: {self.path}\n"
            f"Node Count: {self.node_count}\n"
            f"End Cost (Misplaced): {self.cost_misplaced}\n"
            f"End Cost (Manhattan): {self.cost_manhattan}\n"
            f"End Cost (Euclidean): {self.cost_euclidean}\n"
            f"Initial State (Misplaced): {self.initial_state.cost_misplaced}\n"
            f"Initial State (Manhattan): {self.initial_state.cost_manhattan}\n"
            f"Initial State (Euclidean): {self.initial_state.cost_euclidean}\n"
        )
