from backtracking_algos import NQueensBacktracking as Backtracking
from backtracking_algos import (
    NQueensBacktrackingForwardChecking as BacktrackingForwardChecking,
)
from backtracking_algos import (
    NQueensBacktrackingForwardCheckingMRVLCV as BacktrackingForwardCheckingMRVLCV,
)
from simulated_annealing import SA
from genetic_algorithm import GA


def create_board(dimension):  # Create a board with dimension * dimension
    board = ""
    for i in range(dimension):
        for j in range(dimension):
            board += "Q " if j == i else "# "
        board += "\n"
    return board


def run_ga():
    avg_runtimes_by_n = []
    generations = []
    population = 20
    all_results = []
    for i in range(4, 40):
        print("Dimension: ", i)
        ga = GA(population, i, 0.3)
        ga.start()
        ga.report()
        avg_runtimes_by_n.append(ga.runningTime)
        generations.append(ga.generationNumber)
        all_results.append(
            {
                "Dimension": i,
                "Population": population,
                "Running Time": ga.runningTime,
                "Number of Generations": ga.generationNumber,
            }
        )
        if i > 10:
            population = 50


def run_sa(temperature):
    avg_runtimes_by_n = []
    all_results = []
    for i in range(4, 40):
        sa = SA(temperature, i)
        sa.start()
        sa.report()
        avg_runtimes_by_n.append(sa.runningTime)
        all_results.append(
            {
                "Dimension": i,
                "Temperature": temperature,
                "Running Time": sa.runningTime,
            }
        )


def run_backtracking():
    avg_runtimes_by_n = []
    all_results = []
    for i in range(4, 40):
        print("Dimension: ", i)
        bt = Backtracking(i)
        bt.start()
        bt.report()
        avg_runtimes_by_n.append(bt.runningTime)
        all_results.append(
            {
                "Dimension": i,
                "Running Time": bt.runningTime,
            }
        )


def run_backtracking_forward_checking():
    avg_runtimes_by_n = []
    all_results = []
    for i in range(4, 40):
        print("Dimension: ", i)
        bt = BacktrackingForwardChecking(i)
        bt.start()
        bt.report()
        avg_runtimes_by_n.append(bt.runningTime)
        all_results.append(
            {
                "Dimension": i,
                "Running Time": bt.runningTime,
            }
        )


def run_backtracking_forward_checking_mrv_lcv():
    avg_runtimes_by_n = []
    all_results = []
    for i in range(4, 40):
        print("Dimension: ", i)
        bt = BacktrackingForwardCheckingMRVLCV(i)
        bt.start()
        bt.report()
        avg_runtimes_by_n.append(bt.runningTime)
        all_results.append(
            {
                "Dimension": i,
                "Running Time": bt.runningTime,
            }
        )


def main():
    run_backtracking()
    # run_backtracking_forward_checking()
    # run_backtracking_forward_checking_mrv_lcv()
    # run_sa()
    # run_ga()


if __name__ == "__main__":
    main()
