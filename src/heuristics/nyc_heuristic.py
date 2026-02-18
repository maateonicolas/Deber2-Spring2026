from typing import Dict

def build_heuristic_to_nyc() -> Dict[str, int]:
    """
    h(n): distancia en línea recta (km) a New York City (tabla del PDF).
    """
    return {
        "Elmira": 166,
        "Ithaca": 144,
        "Binghamton": 119,
        "Syracuse": 104,
        "Albany": 63,
        "Scranton": 121,
        "Wilkes-Barre": 73,
        "Allentown": 53,
        "Stroudsburg": 46,
        "Paterson": 21,
        "Newark": 25,
        "Trenton": 45,
        "Philadelphia": 63,
        "Lancaster": 110,
        "Harrisburg": 117,
        "Williamsport": 134,
        "New York City": 0,
    }
