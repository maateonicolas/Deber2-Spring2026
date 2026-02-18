from dataclasses import dataclass

@dataclass
class SearchResult:
    path: list
    cost: int
    generated: int
