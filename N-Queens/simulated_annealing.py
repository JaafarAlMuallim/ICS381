import math
from time import time
from random import randint as rand, uniform
from termcolor import colored


class SA:
    def __init__(
        self,
        dimension,
        initial_temperature=100,
        cooling_rate=0.98,
        min_temperature=1e-5,
    ):
        self.dimension = dimension
        self.board = self.generate_initial_board()
        self.solution = self.board[:]  # Initialize solution with initial board
        self.best_cost = self.cost(self.board)  # Track the best cost
        self.temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.runningTime = 0
        self.expandedNodes = 0
        self.steps = 0
        self.isFound = False
        # New instance variables
        self.is_valid = False
        self.threatening_pairs = self.best_cost
        self.number_of_attacks = 0

    def generate_initial_board(self):
        return [rand(0, self.dimension - 1) for _ in range(self.dimension)]

    def start(self):
        start = time()
        current_state = self.board
        current_cost = self.cost(current_state)

        # Update initial best solution
        self.solution = current_state[:]
        self.best_cost = current_cost
        self.update_validity_status()

        # Check if initial state is already a solution
        if current_cost == 0:
            self.isFound = True
            self.steps = 0
            self.runningTime = 0
            self.expandedNodes = 0
            return

        while self.temperature > self.min_temperature:
            next_state = self.getNeighbor(current_state)
            next_cost = self.cost(next_state)

            # Accept better solutions or worse solutions with a probability based on temperature
            if next_cost < current_cost or self.acceptance_probability(
                current_cost, next_cost
            ):
                current_state = next_state
                current_cost = next_cost

                # Update best solution if current state is better
                if current_cost < self.best_cost:
                    self.solution = current_state[:]
                    self.best_cost = current_cost
                    self.update_validity_status()
                    if current_cost == 0:
                        self.isFound = True
                        break

            # Cool down
            self.temperature *= self.cooling_rate
            self.expandedNodes += 1

        end = time()
        self.runningTime = end - start
        self.board = current_state
        self.steps = self.expandedNodes

    def update_validity_status(self):
        """Update the validity status and threatening pairs count"""
        self.is_valid = self.best_cost == 0
        self.threatening_pairs = self.best_cost

    def getNeighbor(self, state):
        temp_board = state[:]
        i = rand(0, self.dimension - 1)
        j = rand(1, self.dimension - 1)
        temp_board[i] = (temp_board[i] + j) % self.dimension
        return temp_board

    def acceptance_probability(self, current_cost, next_cost):
        # Accept worse solutions with decreasing probability
        if next_cost >= current_cost:
            return math.exp((current_cost - next_cost) / self.temperature) > uniform(
                0, 1
            )
        return True

    def cost(self, state):
        # Calculate the number of attacking pairs of queens
        attacks = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if self.isThreaten(state[i], i, state[j], j):
                    attacks += 1
        self.number_of_attacks = attacks
        return attacks

    def report(self):
        print("Running Time:", self.runningTime, "s")
        print("Number of steps:", self.steps)
        print("Number of Expanded Nodes:", self.expandedNodes)
        print("Best Solution Found:", self.solution)
        print("Best Cost Found:", self.best_cost)
        print("Optimal Solution Found:", self.isFound)
        print("Solution is Valid (No Queens Threatening):", self.is_valid)
        if not self.is_valid:
            print("Number of Threatening Pairs:", self.threatening_pairs)

        print("\nThe Final State:")
        self.constructBoard(self.solution)
        print("= = = = = = = = = = = = = = = = = = = =")

    def constructBoard(self, board):
        finalBoard = [["#"] * self.dimension for _ in range(self.dimension)]
        for i in range(len(board)):
            finalBoard[board[i]][i] = "Q"
        for row in finalBoard:
            for cell in row:
                if cell == "Q":
                    print(colored(cell, "green"), end=" ")
                else:
                    print(cell, end=" ")
            print()

    def isThreaten(self, row1, col1, row2, col2):
        return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)
