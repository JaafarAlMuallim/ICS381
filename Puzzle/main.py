import numpy as np
from math import sqrt

from board import Board
from astar import AStar

goal_puzzle8 = np.append(np.arange(1, 9), 0)
goal_puzzle15 = np.append(np.arange(1, 16), 0)
goal_puzzle24 = np.append(np.arange(1, 25), 0)
goal_puzzle35 = np.append(np.arange(1, 36), 0)


max_mapper = {3: 31, 4: 81, 5: 200, 6: 700}


goal_mapper = {
    3: goal_puzzle8,
    4: goal_puzzle15,
    5: goal_puzzle24,
    6: goal_puzzle35,
}


def generate_board(n=3, method="manhattan"):
    board = np.random.permutation(n**2)
    goal = goal_mapper[n]

    board_obj = Board(goal, board, parent=None, operator=None, method=method)
    if not is_solvable(board_obj):
        return generate_board(n)
    return board


def get_inv_count(state):
    arr = state[state != 0]  # Exclude the blank tile represented by 0
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    return inv_count


def is_solvable(board):
    inv_count = get_inv_count(board.state)
    n = int(sqrt(board.state.shape[0]))
    shaped = board.state.reshape(n, n)
    blank_row = np.where(shaped == 0)[0][0] + 1

    n = sqrt(board.state.shape[0])

    if n % 2 == 1:  # For odd-sized boards
        return inv_count % 2 == 0
    else:  # For even-sized boards
        return ((blank_row + inv_count) % 2) == 0


def main():
    times = 10
    n = 3

    for i in range(times):
        puzzle = generate_board(n)
        print(f"Iteration {i}")
        print(puzzle)
        print(goal_mapper[n])
        board = Board(
            goal_mapper[n],
            puzzle,
            parent=None,
            operator=None,
            method="misplaced",
        )
        x = int(sqrt(len(puzzle) + 1))
        shaped = board.state.reshape(x, x) if board.state is not None else None
        file = open(f"AStar{n}_output.txt", "a+")
        if not is_solvable(board):
            print("Board is not solvable")
            write_empty(file, shaped, get_inv_count(board.state))
            continue

        astar = AStar(board)
        astar.solve()
        print("A* done")
        write_one(file, astar, shaped)

    return 0


# Given an empty board
def write_empty(file, shaped, inv):
    file.write("board: \n" + str(shaped) + "\n")
    file.write("Inversion Count: " + str(inv) + "\n")
    file.close()


# Given a single board
def write_one(file, alg, shaped):
    file.write("Initial State: \n" + str(shaped) + "\n")
    file.write(str(alg) + "\n")
    file.close()


# Given a list of boards
def write_file(file, algs, shaped):
    for i, b in enumerate(algs):
        file.write(f"Initial State: {i}: \n")
        file.write(str(shaped[i]) + "\n")
        if b.solution:
            file.write(str(b) + "\n")
            file.write(
                f"initial_state [misplaced]: "
                + str(b.initial_state.cost_misplaced)
                + "\n"
            )
        file.write(
            f"initial_state [manhattan]: " + str(b.initial_state.cost_manhattan) + "\n"
        )
        file.write(
            f"initial_state [euclidean]: "
            + str(b.initial_state.cost_euclidean)
            + "\n\n\n"
        )
    file.close()


if __name__ == "__main__":
    main()
