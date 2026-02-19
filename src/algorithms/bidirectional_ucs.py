from src.algorithms.priority_queue import RandomTiePriorityQueue
from src.graph.weighted_graph import WeightedGraph
from src.utils.path_utils import reconstruct_path
from src.utils.search_result import SearchResult
from typing import Dict, Optional


class BidirectionalUCS:
    """
    UCS Bidireccional:
      - Dos Dijkstra: uno desde start, otro desde goal.
      - Garantiza óptimo con pesos no negativos.
      - Condición de parada típica: min_f + min_b >= best_solution
    """

    def __init__(self, graph: WeightedGraph, *, verbose: bool = True, seed: int = 0) -> None:
        self.graph = graph
        self.verbose = verbose
        self.seed = seed
        self.generated = 0

    def search(self, start: str, goal: str) -> SearchResult:
        self.generated = 0

        # Distancias y padres
        dist_f: Dict[str, float] = {start: 0.0}
        dist_b: Dict[str, float] = {goal: 0.0}
        parent_f: Dict[str, Optional[str]] = {start: None}
        parent_b: Dict[str, Optional[str]] = {goal: None}

        # PQs
        pq_f = RandomTiePriorityQueue(seed=self.seed)
        pq_b = RandomTiePriorityQueue(seed=self.seed + 1)  # seed distinto para la otra dirección
        pq_f.push(start, 0.0)
        pq_b.push(goal, 0.0)

        best_cost = float("inf")
        meeting: Optional[str] = None

        if self.verbose:
            print("\n" + "=" * 70)
            print("[UCS-BI] Inicio UCS Bidireccional")
            print(f"[UCS-BI] start={start} | goal={goal}")

        # Bucle principal
        while len(pq_f) > 0 and len(pq_b) > 0:
            # Regla de parada (si ya no puedo mejorar)
            if pq_f.peek_priority() + pq_b.peek_priority() >= best_cost:
                if self.verbose:
                    print(f"[UCS-BI] Paro: minF+minB >= best_cost  ({pq_f.peek_priority():.0f}+{pq_b.peek_priority():.0f} >= {best_cost:.0f})")
                break

            # Expandimos el lado que tenga menor frontera (más prometedor)
            if pq_f.peek_priority() <= pq_b.peek_priority():
                self._expand_one_side(
                    side="F",
                    pq=pq_f,
                    dist=dist_f,
                    other_dist=dist_b,
                    parent=parent_f,
                    best_cost_ref=lambda: best_cost,
                    set_best=lambda c, m: (c, m),
                    current_best=(best_cost, meeting),
                )
                # Actualizamos best_cost/meeting desde retorno (porque Python no tiene refs fáciles)
                best_cost, meeting = self._last_best
            else:
                self._expand_one_side(
                    side="B",
                    pq=pq_b,
                    dist=dist_b,
                    other_dist=dist_f,
                    parent=parent_b,
                    best_cost_ref=lambda: best_cost,
                    set_best=lambda c, m: (c, m),
                    current_best=(best_cost, meeting),
                    backward=True,
                )
                best_cost, meeting = self._last_best

        if meeting is None:
            raise RuntimeError("UCS Bidireccional: no se encontró ruta.")

        # Reconstrucción:
        # start -> meeting (usando parent_f)
        path_f = reconstruct_path(parent_f, meeting)

        # meeting -> goal (usando parent_b, pero parent_b fue construido desde goal hacia atrás)
        # parent_b[x] = "padre" en el sentido de la búsqueda hacia atrás, o sea:
        #   en backward, cuando expandimos u (más cerca del goal), y llegamos a v,
        #   parent_b[v] = u   (para que desde meeting puedas caminar hasta goal)
        path_b = []
        cur = meeting
        while cur != goal:
            nxt = parent_b.get(cur)
            if nxt is None:
                # si meeting == goal no entra aquí; si entra, hay inconsistencia
                raise RuntimeError("Reconstrucción backward falló.")
            path_b.append(nxt)
            cur = nxt

        full_path = path_f + path_b
        cost = int(best_cost)

        if self.verbose:
            print(f"[UCS-BI] Mejor ruta: {full_path}")
            print(f"[UCS-BI] Costo óptimo: {cost}")
            print(f"[UCS-BI] Nodos generados: {self.generated}")

        return SearchResult(full_path, cost, self.generated)

    def _expand_one_side(
        self,
        *,
        side: str,
        pq: RandomTiePriorityQueue,
        dist: Dict[str, float],
        other_dist: Dict[str, float],
        parent: Dict[str, Optional[str]],
        best_cost_ref,
        set_best,
        current_best: Tuple[float, Optional[str]],
        backward: bool = False,
    ) -> None:
        """
        Expande 1 nodo del lado F o B.
        backward=False: expansión normal desde start.
        backward=True: expansión desde goal "hacia atrás" (pero el grafo es no dirigido,
                       así que igual recorremos neighbors(u)).
        """
        best_cost, meeting = current_best

        u, g_u = pq.pop()

        # Puede pasar que saquemos un u con costo viejo (ya se mejoró antes)
        if g_u != dist.get(u, float("inf")):
            return

        if self.verbose:
            print(f"\n[UCS-BI] Expando lado {side}: u={u} con g={g_u:.0f}")

        for v, w in self.graph.neighbors(u):
            new_g = g_u + w

            # Genero este vecino (lo intento meter a frontera)
            self.generated += 1
            if self.verbose:
                print(f"  [UCS-BI] Genero {u} -> {v} (w={w}) => g'={new_g:.0f} | generated={self.generated}")

            if new_g < dist.get(v, float("inf")):
                dist[v] = new_g
                pq.push(v, new_g)

                # Padres:
                # - Forward: parent_f[v] = u (normal)
                # - Backward: queremos poder reconstruir meeting -> goal.
                #   Si estamos expandiendo desde el goal, y desde u llegamos a v,
                #   entonces "desde v, el siguiente hacia goal" es u  => parent_b[v] = u
                parent[v] = u

                # Si v ya fue alcanzado por el otro lado, tenemos solución candidata
                if v in other_dist:
                    cand = new_g + other_dist[v]
                    if self.verbose:
                        print(f"    [UCS-BI] 🔁 Encuentro en {v}: cand={cand:.0f} (este lado {new_g:.0f} + otro {other_dist[v]:.0f})")

                    if cand < best_cost:
                        best_cost = cand
                        meeting = v
                        if self.verbose:
                            print(f"    [UCS-BI] Nuevo mejor: best_cost={best_cost:.0f}, meeting={meeting}")

        self._last_best = (best_cost, meeting)