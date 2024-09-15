import numpy as np


class Board:
    parent = None
    state = None
    operator = None
    depth = 0
    zero = None
    n = 0

    def __init__(self, goal, state, parent, operator, method, depth=0):
        self.parent = parent
        self.state = state
        self.operator = operator
        self.depth = depth
        self.method = method
        self.goal = goal
        self.n = int(np.sqrt(len(goal) + 1))
        self.zero = self.find_0()
        self.cost = self.depth + getattr(self, self.method)()
        self.cost_manhattan = self.depth + self.manhattan()
        self.cost_misplaced = self.depth + self.misplaced()
        self.cost_euclidean = self.depth + self.euclidean()

    def goal_test(self):
        if self.state is None:
            return False
        return np.array_equal(self.state, self.goal)

    def find_0(self):
        if self.state is None:
            return None
        for i in range(self.n**2):
            if self.state[i] == 0:
                return i

    @staticmethod
    def index(state):
        index = np.array(range(len(state)))
        for x, y in enumerate(state):
            index[y] = x
        return index

    def swap(self, i, j):
        new_state = np.array(self.state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def up(self):
        if self.zero is None:
            return None
        if self.zero >= self.n:
            return Board(
                self.goal,
                self.swap(self.zero, self.zero - self.n),
                self,
                "Up",
                self.method,
                self.depth + 1,
            )
        else:
            return None

    def down(self):
        if self.zero is None:
            return None
        if self.zero < (self.n * (self.n - 1)):
            return Board(
                self.goal,
                self.swap(self.zero, self.zero + self.n),
                self,
                "Down",
                self.method,
                self.depth + 1,
            )
        else:
            return None

    def left(self):
        if self.zero is None:
            return None
        if self.zero % self.n != 0:
            return Board(
                self.goal,
                self.swap(self.zero, self.zero - 1),
                self,
                "Left",
                self.method,
                self.depth + 1,
            )
        else:
            return None

    def right(self):
        if self.zero is None:
            return None
        if (self.zero + 1) % self.n != 0 and self.zero < self.n**2 - 1:
            return Board(
                self.goal,
                self.swap(self.zero, self.zero + 1),
                self,
                "Right",
                self.method,
                self.depth + 1,
            )
        else:
            return None

    def manhattan(self):
        if self.state is None:
            return 0
        distance = 0
        for i in range(self.n**2):
            if self.state[i] != 0:  # Skip the empty tile
                x, y = divmod(i, self.n)  # Current position of the tile
                goal_value = (
                    (self.state[i] - 1) if self.state[i] != 0 else (self.n**2 - 1)
                )
                x_goal, y_goal = divmod(
                    goal_value, self.n
                )  # Goal position for the tile
                distance += abs(x - x_goal) + abs(y - y_goal)
        return distance

    def misplaced(self):
        if self.state is None:
            return 0
        misplaced_count = 0
        for i in range(self.n**2):
            if self.state[i] != 0 and self.state[i] != i + 1:
                misplaced_count += 1
        return misplaced_count

    def euclidean(self):
        if self.state is None:
            return 0
        distance = 0
        for i in range(self.n**2):
            if self.state[i] != 0:  # Skip the empty tile
                x, y = divmod(i, self.n)  # Current position of the tile
                goal_value = (
                    (self.state[i] - 1) if self.state[i] != 0 else (self.n**2 - 1)
                )
                x_goal, y_goal = divmod(
                    goal_value, self.n
                )  # Goal position for the tile
                distance += np.sqrt((x - x_goal) ** 2 + (y - y_goal) ** 2)
        return distance

    def neighbors(self):
        # Return list of valid neighbors
        neighbors = [self.down(), self.right(), self.up(), self.left()]
        return list(filter(None, neighbors))

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        if self.state is None:
            return "None"
        # Create a string representation for n * n grid
        result = ""
        for i in range(self.n):
            result += str(self.state[i * self.n : (i + 1) * self.n]) + "\n"
        return result + f"Depth: {self.depth}, Operator: {self.operator}\n"

    __repr__ = __str__
