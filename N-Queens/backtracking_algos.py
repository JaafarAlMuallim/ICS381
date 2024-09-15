import time
from termcolor import colored
from collections import defaultdict


class NQueensBacktracking:
    def __init__(self, size):
        self.d = size
        self.solution = []
        self.domains = {i: list(range(size)) for i in range(size)}
        self.isGoal = False
        self.stackDomains = defaultdict(int)
        self.stackVisits = []
        self.runningTime = 0
        self.expandedNodes = 0
        self.steps = 0
        self.visited = {i: [False] * size for i in range(size)}

    def start(self):
        start_time = time.time()
        self.backtrack(0)
        self.runningTime = time.time() - start_time
        self.report()

    def backtrack(self, column):
        if column == self.d:
            self.isGoal = True
            self.solution = self.stackVisits.copy()
            return

        for row in self.domains[column]:
            if not self.visited[column][row]:
                self.visited[column][row] = True
                self.stackVisits.append(row)
                self.stackDomains[column] = row
                if self.isValid(column, row):
                    self.backtrack(column + 1)
                    if self.isGoal:
                        return
                self.visited[column][row] = False
                self.stackVisits.pop()

        self.expandedNodes += 1
        self.steps += 1

    def isValid(self, column, row):
        for i in range(column):
            if self.stackVisits[i] == row or abs(i - column) == abs(
                self.stackVisits[i] - row
            ):
                return False
        return True

    def report(self):
        print("Running Time:", self.runningTime, "s")
        print("Number of steps:", self.steps)
        print("Number of Expanded Nodes:", self.expandedNodes)
        print("The Solution >>", self.solution or "None")
        print("The Final State\n")
        self.constructBoard()
        print("= = = = = = = = = = = = = = = = = = = =")

    def constructBoard(self):
        for i in range(len(self.solution)):
            temp = ["#"] * self.d
            if i in self.solution:
                index = self.solution.index(i)
                temp[index] = "Q"
            for j in range(len(temp)):
                print(
                    (
                        colored(temp[j], self.getColor(j, self.solution))
                        if temp[j] == "Q"
                        else temp[j]
                    ),
                    end=" ",
                )
            print()

    def getColor(self, j, board):
        for col in range(len(board)):
            if col != j and self.isThreaten(board[j], j, board[col], col):
                return "red"
        return "green"

    def isThreaten(self, row1, col1, row2, col2):
        return row1 == row2 or abs(col1 - col2) == abs(row1 - row2)


class NQueensBacktrackingForwardChecking(NQueensBacktracking):
    def __init__(self, size):
        super().__init__(size)

    def start(self):
        start_time = time.time()
        self.forwardCheck(0)
        self.runningTime = time.time() - start_time

    def forwardCheck(self, column):
        if column == self.d:
            self.isGoal = True
            self.solution = self.stackVisits.copy()
            return True  # Indicate that the goal was found

        for row in self.domains[column]:
            if not self.visited[column][row]:
                self.visited[column][row] = True
                self.stackVisits.append(row)
                self.stackDomains[column] = row

                original_domains = {
                    col: self.domains[col][:] for col in range(column + 1, self.d)
                }

                # Prune domains of future columns based on current queen placement
                self.prune_domains(column, row)

                if self.isValid(column, row):
                    if self.forwardCheck(column + 1):  # Check if goal was found
                        return True  # Early exit if solution found

                # Restore domains after backtracking
                self.domains.update(original_domains)

                # Undo changes for this row
                self.visited[column][row] = False
                self.stackVisits.pop()

        self.expandedNodes += 1
        self.steps += 1
        return False  # Indicate that this path did not lead to a solution

    def prune_domains(self, column, row):
        """Remove conflicting rows from the domains of columns ahead."""
        for next_column in range(column + 1, self.d):
            self.domains[next_column] = [
                r
                for r in self.domains[next_column]
                if r != row and abs(next_column - column) != abs(r - row)
            ]


class NQueensBacktrackingForwardCheckingMRVLCV(NQueensBacktrackingForwardChecking):
    def __init__(self, size):
        super().__init__(size)
        self.mrv = {
            i: list(range(self.d)) for i in range(self.d)
        }  # Initial domains for MRV
        self.lcv = defaultdict(list)

    def start(self):
        start_time = time.time()
        self.forwardCheckMRVLCV(0)
        self.runningTime = time.time() - start_time

    def forwardCheckMRVLCV(self, column):
        if column == self.d:
            self.isGoal = True
            self.solution = self.stackVisits.copy()
            return True  # Indicate that the goal was found

        valid_mrv = {k: v for k, v in self.mrv.items() if v}
        if not valid_mrv:
            return False  # No valid moves, backtrack

        rows = sorted(
            self.mrv[column], key=lambda row: len(self.lcv[row]) if self.lcv[row] else 0
        )

        for row in rows:
            if not self.visited[column][row]:
                self.visited[column][row] = True
                self.stackVisits.append(row)
                self.stackDomains[column] = row

                original_mrv = {
                    col: self.mrv[col][:] for col in range(column + 1, self.d)
                }
                original_lcv = {key: self.lcv[key][:] for key in self.lcv}

                self.updateMRVLCV(column, row)

                if self.isValid(column, row):
                    if self.forwardCheckMRVLCV(column + 1):  # Check if goal was found
                        return True  # Early exit if solution found

                # Restore MRV and LCV on backtracking
                self.mrv.update(original_mrv)
                self.lcv = defaultdict(
                    list, original_lcv
                )  # Restore LCV with previous state
                self.visited[column][row] = False
                self.stackVisits.pop()

        self.expandedNodes += 1
        self.steps += 1
        return False  # Indicate that this path did not lead to a solution

    def updateMRVLCV(self, column, row):
        """Update MRV and LCV based on the current placement."""
        for next_column in range(column + 1, self.d):
            self.mrv[next_column] = [
                r
                for r in self.mrv[next_column]
                if r != row and abs(next_column - column) != abs(r - row)
            ]

            self.lcv = defaultdict(list)  # Reset LCV to avoid residual values
            for r in self.mrv[next_column]:
                self.lcv[r] = [
                    r2
                    for r2 in self.mrv[next_column]
                    if r2 != r and abs(next_column - column) == abs(r2 - r)
                ]
