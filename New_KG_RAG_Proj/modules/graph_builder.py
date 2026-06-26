import networkx as nx

def create_graph(links):

    G = nx.DiGraph()

    for source, relation, target in links:

        G.add_node(source)

        G.add_node(target)

        G.add_edge(
            source,
            target,
            relation=relation
        )

    return G