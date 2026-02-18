from graph.deber_graph import build_deber_graph
from heuristics.nyc_heuristic import build_heuristic_to_nyc
from algorithms.iddfs import IDDFS
from algorithms.bidirectional_ucs import BidirectionalUCS
from algorithms.astar import AStar
from config import *

def main():
    graph = build_deber_graph()
    heuristic = build_heuristic_to_nyc()

    iddfs = IDDFS(graph, verbose=VERBOSE)
    res1 = iddfs.search(START_NODE, GOAL_NODE, MAX_DEPTH_IDDFS)

    ucs = BidirectionalUCS(graph, verbose=VERBOSE, seed=RANDOM_SEED)
    res2 = ucs.search(START_NODE, GOAL_NODE)

    astar = AStar(graph, heuristic, verbose=VERBOSE, seed=RANDOM_SEED)
    res3 = astar.search(START_NODE, GOAL_NODE)

if __name__ == "__main__":
    main()
