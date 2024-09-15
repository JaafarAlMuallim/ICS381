from abc import ABC, abstractmethod


class Solver(ABC):
    solution = None
    frontier = None
    nodes_expanded = 0
    expanded_nodes = set()
    max_depth = 0
    explored_nodes = set()
    initial_state = None

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.nodes_expanded = 0

    def ancestral_chain(self):
        current = self.solution if self.solution else None
        chain = [current]
        if current is None:
            return chain
        while current.parent is not None:
            chain.append(current.parent)
            current = current.parent
        return chain

    @property
    def path(self):
        path = [
            node.operator for node in self.ancestral_chain()[-2::-1] if node is not None
        ]
        return path

    @abstractmethod
    def solve(self):
        pass

    def set_solution(self, board):
        self.solution = board
        # length = len(self.frontier) if self.frontier is not None else 0
        # self.nodes_expanded = len(self.explored_nodes) - length - 1
        return self.solution
