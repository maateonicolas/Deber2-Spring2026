from .weighted_graph import WeightedGraph

def build_deber_graph():
    g = WeightedGraph()

    # Lado izquierdo / centro
    g.add_edge("Elmira", "Ithaca", 60)
    g.add_edge("Elmira", "Williamsport", 80)
    g.add_edge("Ithaca", "Binghamton", 80)
    g.add_edge("Binghamton", "Syracuse", 110)
    g.add_edge("Syracuse", "Albany", 200)
    g.add_edge("Binghamton", "Albany", 220)
    g.add_edge("Binghamton", "Scranton", 95)

    # Centro / derecha
    g.add_edge("Scranton", "Wilkes-Barre", 30)
    g.add_edge("Wilkes-Barre", "Stroudsburg", 105)
    g.add_edge("Stroudsburg", "Albany", 190)
    g.add_edge("Stroudsburg", "Paterson", 90)
    g.add_edge("Paterson", "New York City", 35)

    # Centro / abajo-derecha
    g.add_edge("Wilkes-Barre", "Allentown", 95)
    g.add_edge("Scranton", "Allentown", 120)
    g.add_edge("Allentown", "Newark", 80)
    g.add_edge("Newark", "New York City", 25)

    g.add_edge("Allentown", "Trenton", 130)
    g.add_edge("Trenton", "New York City", 95)

    # Abajo
    g.add_edge("Trenton", "Philadelphia", 50)
    g.add_edge("Allentown", "Philadelphia", 90)
    g.add_edge("Harrisburg", "Philadelphia", 160)
    g.add_edge("Harrisburg", "Lancaster", 60)
    g.add_edge("Lancaster", "Philadelphia", 110)

    # Centro-izquierda / abajo
    g.add_edge("Williamsport", "Scranton", 140)
    g.add_edge("Williamsport", "Harrisburg", 135)
    g.add_edge("Scranton", "Harrisburg", 175)

    return g
