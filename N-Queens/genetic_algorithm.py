from random import shuffle, randint as rand, random
from time import time
from termcolor import colored
from board import Board


class GA:
    def __init__(self, population, dimension, crossover=0.3):
        self.generationNumber = 1
        self.pSize = population
        self.d = dimension
        self.co = crossover
        self.crossover = crossover
        self.environment = []
        self.solved = False
        self.solution = None
        self.minCosts = []
        self.runningTime = 0
        self.expandedNodes = population
        self.stagnant_generations = 0  # Track stagnation

    def start(self):
        start = time()
        self.initializeEnvironment()
        self.checkGoal()
        self.co = 0.3

        while not self.solved:
            self.generationNumber += 1
            previous_min_cost = min(self.minCosts) if self.minCosts else float("inf")
            self.crossOver()
            self.updateEnvironment()
            self.checkGoal()

            # Check for stagnation and increase mutation rate if needed
            current_min_cost = min(self.minCosts)
            if current_min_cost >= previous_min_cost:
                self.stagnant_generations += 1
            else:
                self.stagnant_generations = 0

            if self.stagnant_generations > 5:  # Adjust mutation rate if stuck
                print(
                    f"Increasing mutation rate due to stagnation {self.co} {self.pSize} {self.d} {current_min_cost}"
                )
                self.co = min(
                    self.co + 0.1, 0.9
                )  # Temporarily increase crossover/mutation variability
                self.stagnant_generations = 0

        end = time()
        self.runningTime = end - start
        self.expandedNodes = len(self.environment)

    def initializeEnvironment(self):
        for _ in range(self.pSize):
            chrom = list(range(self.d))
            shuffle(chrom)
            while chrom in self.environment:
                shuffle(chrom)
            self.environment.append(chrom)

    def checkGoal(self):
        for chrom in self.environment:
            state = Board(chrom)
            if state.cost == 0:
                self.solved = True
                self.solution = chrom
                break

    def crossOver(self):
        new_chromosomes = []
        elite_chromosomes = sorted(
            self.environment, key=lambda chrom: Board(chrom).cost
        )[:2]

        for i in range(0, len(self.environment) - 1, 2):
            chrom1, chrom2 = self.environment[i][:], self.environment[i + 1][:]
            child1, child2 = self.orderCrossover(chrom1, chrom2)
            self.mutant(child1)
            self.mutant(child2)
            new_chromosomes.extend([child1, child2])

        self.environment = elite_chromosomes + new_chromosomes  # Retain elites

    def orderCrossover(self, parent1, parent2):
        start, end = sorted([rand(0, self.d - 1) for _ in range(2)])
        child1, child2 = [-1] * self.d, [-1] * self.d

        # Copy slice from parents
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        # Fill remaining slots to avoid duplicate genes
        def fill_positions(child, parent):
            remaining_genes = [gene for gene in parent if gene not in child[start:end]]
            for i in range(self.d):
                if child[i] == -1:
                    child[i] = remaining_genes.pop(0)
            return child

        child1 = fill_positions(child1, parent2)
        child2 = fill_positions(child2, parent1)

        # Additional random swaps to introduce diversity
        if random() < 0.2:  # 20% chance to swap genes
            idx1, idx2 = rand(0, self.d - 1), rand(0, self.d - 1)
            child1[idx1], child1[idx2] = child1[idx2], child1[idx1]
            child2[idx1], child2[idx2] = child2[idx2], child2[idx1]

        return child1, child2

    def mutant(self, chrom):
        mutation_rate = 0.3  # Define mutation rate (30%)
        if random() < mutation_rate:
            self.mutantSwap(chrom)

    def mutantSwap(self, chrom):
        left_index, right_index = rand(0, self.d - 1), rand(0, self.d - 1)
        chrom[left_index], chrom[right_index] = chrom[right_index], chrom[left_index]

    def updateEnvironment(self):
        costs = [(Board(chrom).cost, chrom) for chrom in self.environment]
        costs.sort(key=lambda x: x[0])

        # Retain only the best chromosomes to control population size
        self.environment = [chrom for _, chrom in costs[: self.pSize]]
        self.minCosts = [cost for cost, _ in costs[: self.pSize]]

        if min(self.minCosts) == 0:
            self.solved = True
            self.solution = self.environment[self.minCosts.index(0)]

    def report(self):
        print("Running Time:", self.runningTime, "s")
        print("Number of Generations:", self.generationNumber)
        print("Number of Expanded Nodes:", self.expandedNodes)
        print("Solution:", self.solution)
        print("Final State\n")
        self.constructBoard()

    def constructBoard(self):
        if not isinstance(self.solution, list):
            return
        for i in range(self.d):
            row = ["#"] * self.d
            index = self.solution.index(i)
            row[index] = "Q"
            for j, cell in enumerate(row):
                color = self.getColor(j, self.solution) if cell == "Q" else None
                print(colored(cell, color) if color else cell, end=" ")
            print()

    def getColor(self, j, board):
        for col in range(len(board)):
            if col != j and self.isThreaten(board[j], j, board[col], col):
                return "red"
        return "green"

    def isThreaten(self, i, x, j, y):
        return i == j or x == y or abs(i - j) == abs(x - y)
