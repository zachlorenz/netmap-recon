# netmap/graph.py
import matplotlib
matplotlib.use("Agg")

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict
from matplotlib.lines import Line2D
from netmap.utils import annotate_roles

ROLE_STYLE = {
    "router": {"shape": "^", "color": "#ffcc80"},  # orange triangle
    "server": {"shape": "s", "color": "#bbdefb"},  # blue square
    "dns":    {"shape": "D", "color": "#c5e1a5"},  # green diamond
    "web":    {"shape": "h", "color": "#ffe082"},  # amber hex
    "db":     {"shape": "s", "color": "#d7ccc8"},  # brown square
    "ldap":   {"shape": "s", "color": "#c5cae9"},  # indigo square
    "ssh":    {"shape": "s", "color": "#b2dfdb"},  # teal square
    "rdp":    {"shape": "s", "color": "#f8bbd0"},  # pink square
    "host":   {"shape": "o", "color": "#e3f2fd"},  # light blue circle
}

def build_graph(edges: List[Dict]) -> nx.DiGraph:
    G = nx.DiGraph()
    for e in edges:
        src = e["src"]; dst = e["dst"]
        # create nodes
        if src not in G: G.add_node(src, type="ip")
        if dst not in G: G.add_node(dst, type="service" if (":" in dst and "/" in dst) else "ip")
        # create edge with label
        label = f"{e.get('proto','')}/{e.get('dport','')}" if e.get('dport') else e.get('proto', '')
        G.add_edge(src, dst, label=label)
    # annotate roles AFTER graph is built
    annotate_roles(G, edges)
    return G

def _partition_by_role(G, pos):
    buckets = {}
    for n, data in G.nodes(data=True):
        role = data.get("role", "host")
        buckets.setdefault(role, {"nodes": [], "pos": {}})
        buckets[role]["nodes"].append(n)
        buckets[role]["pos"][n] = pos[n]
    return buckets

def draw_graph(G: nx.DiGraph, out_png: str = "docs/map.png") -> None:
    plt.figure(figsize=(13, 9))

    if G.number_of_nodes() == 0:
        plt.text(0.5, 0.5, "No edges detected.\nTry --proto any or a different PCAP.",
                 ha="center", va="center", fontsize=16)
        plt.axis("off"); plt.tight_layout(); plt.savefig(out_png, dpi=220); plt.close(); return

    # layout
    pos = nx.spring_layout(G, seed=42, k=0.7)

    # edges & labels first (under nodes)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=12, width=1.2, alpha=0.7)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)

    # group nodes by role and draw with different shapes/colors
    buckets = _partition_by_role(G, pos)
    for role, data in buckets.items():
        style = ROLE_STYLE.get(role, ROLE_STYLE["host"])
        nx.draw_networkx_nodes(
            G,
            data["pos"],
            nodelist=data["nodes"],
            node_shape=style["shape"],
            node_color=style["color"],
            edgecolors="#263238",
            linewidths=1.2,
            alpha=0.95,
            node_size=800
        )

    # labels last for clarity
    nx.draw_networkx_labels(G, pos, font_size=9)

    # legend
    handles = []
    for role, style in [("router","^"),("server","s"),("dns","D"),("web","h"),("host","o")]:
        color = ROLE_STYLE[role]["color"]
        handles.append(Line2D([0],[0], marker=style, color="w", label=role.upper(),
                              markerfacecolor=color, markeredgecolor="#263238", markersize=12))
    plt.legend(handles=handles, loc="lower left", frameon=True)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_png, dpi=220)
    plt.close()
