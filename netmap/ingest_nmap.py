import xml.etree.ElementTree as ET
from typing import List, Dict

def build_edges_from_nmap(xml_path: str) -> List[Dict]:
    """
    Parse Nmap XML and return edges as service connections from host -> service node.
    For MVP we create edges host_ip -> "host_ip:port/PROTO" to visualize exposure.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    edges: List[Dict] = []
    for host in root.findall('host'):
        addr = host.find("address[@addrtype='ipv4']")
        if addr is None:
            continue
        ip = addr.get('addr')

        ports = host.find('ports')
        if ports is None:
            continue

        for port in ports.findall('port'):
            proto = (port.get('protocol') or '').upper()
            portid = port.get('portid')
            state = port.find('state')
            if state is None or state.get('state') != 'open':
                continue
            service = port.find('service')
            banner = service.get('product') if (service is not None and service.get('product')) else ''

            svc_node = f"{ip}:{portid}/{proto or 'TCP'}"
            edges.append({
                "src": ip,
                "dst": svc_node,
                "sport": 0,
                "dport": int(portid) if portid and portid.isdigit() else 0,
                "proto": proto or "TCP",
                "banner": banner
            })
    return edges
