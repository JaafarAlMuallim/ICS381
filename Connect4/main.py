import pandas as pd
from agents import *
from game_simulator import GameSimulator


def main():
    simulator = GameSimulator()
    sets = [
        (MiniMaxAgent(1), MiniMaxAgent(2), "set1"),
        (MiniMaxAgent(1), ExpectiMaxAgent(2, 0.5), "set2"),
        (MiniMaxAgent(1), RandomAgent(2), "set3"),
        (ExpectiMaxAgent(1, 0.75), RandomAgent(2), "set4"),
        (ExpectiMaxAgent(1, 0.5), RandomAgent(2), "set5"),
        (ExpectiMaxAgent(1, 0.25), RandomAgent(2), "set6"),
    ]

    for p1, p2, set_name in sets:
        simulator.run_set(p1, p2, 10, set_name)

    ## slice the data to get results of each set
    set1 = simulator.data[:10]
    set2 = simulator.data[10:20]
    set3 = simulator.data[20:30]
    set4 = simulator.data[30:40]
    set5 = simulator.data[40:50]
    set6 = simulator.data[50:60]
    setx = [set1, set2, set3, set4, set5, set6]

    ## create dataframe to analyze each set by finding average, max, min score for each agent
    for i, s in enumerate(setx):
        print(f"Most wins in set {i+1}")
        print(pd.DataFrame(s)["Winner"].value_counts())
        print("\n")
        df = pd.DataFrame(s)
        print(f"Set {i+1}")
        ## append file set{i+1}.xlsx with description
        with pd.ExcelWriter(f"set{i+1}_analysis.xlsx") as writer:
            df.to_excel(writer, sheet_name="data")
            df.describe().to_excel(writer, sheet_name="description")

    pd.DataFrame(simulator.data).to_excel("all_results.xlsx")


if __name__ == "__main__":
    main()
