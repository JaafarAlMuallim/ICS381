# from .human import HumanAgent
from .random import RandomAgent
from .lookahead import LookAheadAgent
from .minimax import MiniMaxAgent
from .expectimax import ExpectiMaxAgent
from .montecarlo import MonteCarloAgent

__all__ = [
    # "HumanAgent",
    "RandomAgent",
    "LookAheadAgent",
    "MiniMaxAgent",
    "ExpectiMaxAgent",
    "MonteCarloAgent",
]
