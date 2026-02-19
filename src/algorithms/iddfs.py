from src.graph.weighted_graph import WeightedGraph
from src.utils.path_utils import path_cost
from src.utils.search_result import SearchResult


class IDDFS:
    """
    Iterative Deepening DFS:
      - Hace DFS con límite de profundidad 0,1,2,...
      - No garantiza costo mínimo (porque optimiza profundidad, no peso)
    """

    def __init__(self, graph: WeightedGraph, *, verbose: bool = True) -> None:
        self.graph = graph
        self.verbose = verbose
        self.generated = 0

    def search(self, start: str, goal: str, max_depth: int = 50) -> SearchResult:
        self.generated = 0

        for depth_limit in range(max_depth + 1):
            if self.verbose:
                print("\n" + "=" * 70)
                print(f"[IDDFS] Iteración con depth_limit = {depth_limit}")

            found = self._dls(
                current=start,
                goal=goal,
                depth_limit=depth_limit,
                path=[start],
                in_path={start},
            )
            if found is not None:
                cost = path_cost(self.graph, found)
                if self.verbose:
                    print(f"[IDDFS] Encontrado en límite {depth_limit}: {found} | costo={cost}")
                    print(f"[IDDFS] Nodos generados: {self.generated}")
                return SearchResult(found, cost, self.generated)

        raise RuntimeError(f"IDDFS: No se encontró solución hasta max_depth={max_depth}")

    def _dls(
        self,
        current: str,
        goal: str,
        depth_limit: int,
        path: List[str],
        in_path: Set[str],
    ) -> Optional[List[str]]:
        """
        Depth-Limited Search (DFS con límite).
        """
        if self.verbose:
            print(f"[IDDFS] Visitando: {current} | profundidad restante: {depth_limit} | path={path}")

        if current == goal:
            return path

        if depth_limit == 0:
            return None

        # Para reproducibilidad, recorremos vecinos en orden alfabético por nombre
        for (nbr, w) in sorted(self.graph.neighbors(current), key=lambda x: x[0]):
            if nbr in in_path:
                continue  # evitar ciclos simples en el camino actual

            # "Generado" = creo un hijo candidato para explorar
            self.generated += 1
            if self.verbose:
                print(f"  [IDDFS] Genero hijo: {current} -> {nbr} (costo arista {w}) | generated={self.generated}")

            in_path.add(nbr)
            res = self._dls(nbr, goal, depth_limit - 1, path + [nbr], in_path)
            in_path.remove(nbr)

            if res is not None:
                return res

        return None