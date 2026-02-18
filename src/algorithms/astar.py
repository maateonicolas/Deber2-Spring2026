from src.algorithms.priority_queue import RandomTiePriorityQueue
from src.graph.weighted_graph import WeightedGraph
from src.utils.path_utils import reconstruct_path
from src.utils.search_result import SearchResult
from typing import Dict, Optional


class AStar:
    """
    A*:
      f(n) = g(n) + h(n)
      - Con h admisible => óptimo.
    """

    def __init__(self, graph: WeightedGraph, heuristic: Dict[str, int], *, verbose: bool = True, seed: int = 0) -> None:
        self.graph = graph
        self.h = heuristic
        self.verbose = verbose
        self.seed = seed
        self.generated = 0

    def search(self, start: str, goal: str) -> SearchResult:
        self.generated = 0

        pq = RandomTiePriorityQueue(seed=self.seed)
        pq.push(start, self.h[start])  # f = 0 + h(start)

        g_cost: Dict[str, float] = {start: 0.0}
        parent: Dict[str, Optional[str]] = {start: None}
        closed: Set[str] = set()

        if self.verbose:
            print("\n" + "=" * 70)
            print("[A*] Inicio A*")
            print(f"[A*] start={start} | goal={goal}")

        while len(pq) > 0:
            u, f_u = pq.pop()

            if u in closed:
                continue
            closed.add(u)

            if self.verbose:
                print(f"\n[A*] Pop u={u} | f={f_u:.0f} | g={g_cost[u]:.0f} | h={self.h.get(u, 0)}")

            if u == goal:
                path = reconstruct_path(parent, goal)
                cost = int(g_cost[goal])
                if self.verbose:
                    print(f"[A*] ✅ Encontrado goal: {path} | costo={cost}")
                    print(f"[A*] Nodos generados: {self.generated}")
                return SearchResult(path, cost, self.generated)

            for v, w in self.graph.neighbors(u):
                new_g = g_cost[u] + w

                # Generamos este vecino (lo evaluamos para frontera)
                self.generated += 1
                if self.verbose:
                    print(f"  [A*] Genero {u} -> {v} (w={w}) => g'={new_g:.0f} | generated={self.generated}")

                if v in closed and new_g >= g_cost.get(v, float("inf")):
                    continue

                if new_g < g_cost.get(v, float("inf")):
                    g_cost[v] = new_g
                    parent[v] = u
                    f_v = new_g + self.h.get(v, 0)
                    pq.push(v, f_v)

                    if self.verbose:
                        print(f"    [A*] Push {v} con f={f_v:.0f} (g={new_g:.0f}+h={self.h.get(v, 0)})")

        raise RuntimeError("A*: No se encontró ruta.")