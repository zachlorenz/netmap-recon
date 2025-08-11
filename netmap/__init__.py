ingest_pcap_py = r'''import pyshark

def _display_filter(proto: str) -> str | None:
    if proto == "dns":
        return "dns"
    if proto == "http":
        return "http"
    if proto == "tcp":
        return "tcp && tcp.len > 0"
    if proto == "udp":
        return "udp"
    return None


def build_edges_from_pcap(pcap_path: str, proto: str = "any", packet_limit: int | None = None):
    """
    Return a list of edges as dicts: {"src": ip, "dst": ip, "sport": int, "dport": int, "proto": "TCP|UDP"}
    """
    dfilter = _display_filter(proto)
    kwargs = dict(keep_packets=False, use_json=True, include_raw=False, custom_parameters=['-n'])
    if packet_limit:
        kwargs["packet_count"] = packet_limit

    cap = pyshark.FileCapture(pcap_path, display_filter=dfilter, **kwargs) if dfilter else pyshark.FileCapture(pcap_path, **kwargs)

    edges = []
    for pkt in cap:
        try:
            src = pkt.ip.src
            dst = pkt.ip.dst
        except Exception:
            continue

        if hasattr(pkt, 'tcp'):
            try:
                sport = int(pkt.tcp.srcport)
                dport = int(pkt.tcp.dstport)
            except Exception:
                continue
            proto_name = "TCP"
        elif hasattr(pkt, 'udp'):
            try:
                sport = int(pkt.udp.srcport)
                dport = int(pkt.udp.dstport)
            except Exception:
                continue
            proto_name = "UDP"
        else:
            # Skip non TCP/UDP for MVP
            continue

        edges.append({"src": src, "dst": dst, "sport": sport, "dport": dport, "proto": proto_name})

    cap.close()
    return edges
'''
