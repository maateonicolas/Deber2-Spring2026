from src.graph.weighted_graph import WeightedGraph
from typing import Dict, Optional


def path_cost(graph: WeightedGraph, path: List[str]) -> int:
    """
    Suma los pesos de las aristas en el path.
    """
    total = 0
    for a, b in zip(path, path[1:]):
        # buscar peso a->b
        for (nbr, w) in graph.neighbors(a):
            if nbr == b:
                total += w
                break
        else:
            raise ValueError(f"No existe arista {a} -> {b} en el grafo.")
    return total


def reconstruct_path(parents: Dict[str, Optional[str]], goal: str) -> List[str]:
    """
    Reconstruye un camino usando un diccionario de padres:
      parents[node] = parent_node, parents[start] = None
    """
    out = []
    cur = goal
    while cur is not None:
        out.append(cur)
        cur = parents[cur]
    out.reverse()
    return out