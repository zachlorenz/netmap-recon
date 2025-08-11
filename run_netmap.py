#!/usr/bin/env python3
import argparse
from netmap.ingest_pcap import build_edges_from_pcap
from netmap.graph import build_graph, draw_graph
from netmap.report import write_nodes_csv, write_edges_csv, write_json


def parse_args():
    p = argparse.ArgumentParser(description="NetMap-Recon: Build a logical service map from PCAP or Nmap inputs.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--pcap", help="Path to pcap/pcapng file")
    src.add_argument("--nmap-xml", dest="nmap_xml", help="Path to nmap XML output (optional input mode)")

    p.add_argument("--proto", choices=["any", "tcp", "udp", "dns", "http"], default="any", help="Filter PCAP by protocol (PCAP mode)")
    p.add_argument("--limit", type=int, default=None, help="Optional packet limit for fast tests (PCAP mode)")

    p.add_argument("--out-graph", default="docs/map.png", help="Output PNG path for the topology graph")
    p.add_argument("--out-nodes", default="nodes.csv", help="Output CSV of nodes")
    p.add_argument("--out-edges", default="edges.csv", help="Output CSV of edges")
    p.add_argument("--out-json", default="map.json", help="Output JSON with nodes+edges")
    return p.parse_args()


def main():
    args = parse_args()

    if args.pcap:
        print(f"[+] Ingesting PCAP: {args.pcap}")
        edges = build_edges_from_pcap(args.pcap, proto=args.proto, packet_limit=args.limit)
    else:
        from netmap.ingest_nmap import build_edges_from_nmap
        print(f"[+] Ingesting Nmap XML: {args.nmap_xml}")
        edges = build_edges_from_nmap(args.nmap_xml)

    print(f"[+] Edges discovered: {len(edges)}")
    G = build_graph(edges)

    # Exports
    draw_graph(G, args.out_graph)
    write_nodes_csv(G, args.out_nodes)
    write_edges_csv(edges, args.out_edges)
    write_json(G, edges, args.out_json)

    print("[+] Outputs written:")
    print(f"    Graph: {args.out_graph}")
    print(f"    Nodes: {args.out_nodes}")
    print(f"    Edges: {args.out_edges}")
    print(f"    JSON : {args.out_json}")


if __name__ == "__main__":
    main()

