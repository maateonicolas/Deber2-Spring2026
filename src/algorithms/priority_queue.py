import heapq
import random

class RandomTiePriorityQueue:
    def __init__(self, seed=0):
        self.heap = []
        self.rng = random.Random(seed)
        self.counter = 0

    def push(self, node, priority):
        self.counter += 1
        tie = self.rng.random()
        heapq.heappush(self.heap, (priority, tie, self.counter, node))

    def pop(self):
        priority, tie, seq, node = heapq.heappop(self.heap)
        return node, priority

    def peek_priority(self):
        if not self.heap:
            return float("inf")
        return self.heap[0][0]

    def __len__(self):
        return len(self.heap)
