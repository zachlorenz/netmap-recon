# netmap/utils.py
from ipaddress import ip_address
from collections import defaultdict

COMMON_PORT_ROLES = {
    53: "dns",
    80: "web",
    443: "web",
    8080: "web",
    8443: "web",
    389: "ldap",
    636: "ldap",
    1433: "db",
    1521: "db",
    3306: "db",
    5432: "db",
    22: "ssh",
    3389: "rdp",
}

def _is_ip(s: str) -> bool:
    try:
        ip_address(s)
        return True
    except Exception:
        return False

def _subnet24(ip: str) -> str:
    # crude /24 key
    parts = ip.split(".")
    return ".".join(parts[:3]) if len(parts) == 4 else ip

def annotate_roles(G, edges):
    """
    Annotate each node with a 'role' attribute based on heuristics:
    - service nodes like "10.0.0.5:443/TCP" -> role from port map or 'server'
    - plain IP nodes:
       * 'router' if connects across >= 3 distinct /24 subnets or degree >= 8
       * else 'host'
    """
    # 1) mark service nodes from edges
    for e in edges:
        dst = e.get("dst", "")
        dport = e.get("dport")
        if ":" in dst and "/" in dst:
            role = COMMON_PORT_ROLES.get(dport, "server")
            G.nodes[dst]["role"] = role

    # 2) evaluate plain IP nodes
    for n in G.nodes():
        if G.nodes[n].get("role"):
            continue
        if _is_ip(n):
            # how many distinct /24s does this node connect to?
            neigh_subnets = set()
            for nbr in set(list(G.predecessors(n)) + list(G.successors(n))):
                ip = nbr.split(":")[0] if ":" in nbr else nbr
                if _is_ip(ip):
                    neigh_subnets.add(_subnet24(ip))
            deg = G.degree(n)
            if len(neigh_subnets) >= 3 or deg >= 8:
                G.nodes[n]["role"] = "router"
            else:
                G.nodes[n]["role"] = "host"
        else:
            # non-ip non-service (shouldn't happen often)
            G.nodes[n]["role"] = "server"

    return G
