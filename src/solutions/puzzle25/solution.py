import networkx as nx

def main(input_file):
    lines = [l for l in input_file.split("\n") if len(l) > 0]
    d = {}
    for l in lines:
        k, v = l.split(": ")
        d[k] = v.split(" ")

    G = nx.Graph()
    for k, v in d.items():
        for k2 in v:
            G.add_edge(k, k2)

    edges_to_remove = nx.minimum_edge_cut(G)
    G.remove_edges_from(edges_to_remove)
    groups = list(nx.connected_components(G))
    pt1_ans = len(groups[0]) * len(groups[1])
    return (pt1_ans,)