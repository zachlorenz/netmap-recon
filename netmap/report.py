import json
import csv
from typing import List, Dict
import networkx as nx

def write_nodes_csv(G: nx.DiGraph, out_csv: str) -> None:
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["node", "type"])
        for n, data in G.nodes(data=True):
            w.writerow([n, data.get('type', '')])

def write_edges_csv(edges: List[Dict], out_csv: str) -> None:
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["src", "dst", "sport", "dport", "proto"])
        for e in edges:
            w.writerow([e.get('src',''), e.get('dst',''), e.get('sport',''), e.get('dport',''), e.get('proto','')])

def write_json(G: nx.DiGraph, edges: List[Dict], out_json: str) -> None:
    doc = {
        "nodes": [{"id": n, **data} for n, data in G.nodes(data=True)],
        "edges": edges,
        "stats": {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges()
        }
    }
    with open(out_json, 'w') as f:
        json.dump(doc, f, indent=2)
