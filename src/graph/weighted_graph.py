class WeightedGraph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, w):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, node):
        return self.adj.get(node, [])
