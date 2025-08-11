# 🗺️ NetMap-Recon

**Network mapping & visualization from PCAP or Nmap.**  
Turns raw traffic or scan results into a clean service map (PNG), plus CSV/JSON inventories you can fuse with other tools.

> Built to showcase DNEA-relevant skills: passive/active recon, flow extraction, role heuristics (router/server/host), and analyst-ready reporting.

---

## ✨ Features

- **PCAP ingest (PyShark/tshark):** extract IP↔service edges (TCP/UDP/DNS/HTTP filters)
- **Nmap ingest (XML):** convert scan results into service nodes (with banners)
- **Auto role labeling:** router/server/host + common roles (web/dns/db/ldap/ssh/rdp)
- **Graph output:** `docs/map.png` with distinct node shapes/colors + legend
- **Artifacts:** `nodes.csv`, `edges.csv`, and `map.json` for downstream fusion
- **Headless-safe:** Works in WSL/servers; no GUI needed (matplotlib Agg backend)

---

## 📂 Repository Structure

netmap-recon/
├── run_netmap.py
├── netmap/
│ ├── init.py
│ ├── ingest_pcap.py
│ ├── ingest_nmap.py
│ ├── graph.py
│ ├── report.py
│ ├── enrich.py
│ └── utils.py
├── docs/
│ ├── detection_flow.png # (optional workflow diagram)
│ └── map.png # generated topology graph
├── example/
│ └── sample.pcap # add your test pcaps here
├── requirements.txt
└── README.md


---

## ⚙️ Installation

```bash
# From repo root
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt update && sudo apt install -y tshark   # PyShark backend
If using WSL/Kali, keep your repo & pcaps on Linux side (e.g., ~/netmap-recon) for speed.

🚀 Quickstart
# Example with a small UDP-heavy PCAP (e.g., DHCP/DNS)
python run_netmap.py \
  --pcap example/sample.pcap \
  --proto udp \
  --out-graph docs/map.png \
  --out-nodes docs/nodes.csv \
  --out-edges docs/edges.csv \
  --out-json  docs/map.json

# Open the outputs (WSL)
explorer.exe docs
🧭 Full CLI Usage (Cheat Sheet)
python run_netmap.py (--pcap PATH | --nmap-xml PATH)
                     [--proto {any,tcp,udp,dns,http}]
                     [--limit INT]
                     [--out-graph PATH]
                     [--out-nodes PATH]
                     [--out-edges PATH]
                     [--out-json PATH]
Required (choose one)
--pcap PATH — analyze a PCAP/PCAPNG file

--nmap-xml PATH — analyze an Nmap XML scan (nmap -oX scan.xml ...)

Optional (PCAP mode)
--proto {any,tcp,udp,dns,http} (default any) — display filter during ingest

--limit INT — cap packet count for fast testing

Outputs (defaults shown)
--out-graph docs/map.png — PNG topology graph

--out-nodes nodes.csv — node inventory (type/role)

--out-edges edges.csv — edges (src,dst,ports,proto)

--out-json map.json — nodes + edges + stats in one JSON

Common commands
PCAP quick run

python run_netmap.py --pcap example/sample.pcap
UDP-only (DHCP/DNS)

python run_netmap.py --pcap example/sample.pcap --proto udp
TCP-only (HTTP/HTTPS)

python run_netmap.py --pcap example/http.cap --proto tcp
DNS-only

python run_netmap.py --pcap example/dns.cap --proto dns
Speed test on big PCAP

python run_netmap.py --pcap example/big.pcap --proto any --limit 20000
Nmap XML mode

nmap -sS -sV -oX example/scan.xml 192.168.1.0/24
python run_netmap.py --nmap-xml example/scan.xml \
  --out-graph docs/map.png --out-nodes docs/nodes.csv --out-edges docs/edges.csv --out-json docs/map.json
🖼️ Example Output
Graph (docs/map.png)

Routers = ▲ (orange)

Servers = ■ (blue)

DNS = ◆ (green)

Web = ⬢ (amber)

Hosts = ● (light blue)

Edge labels = PROTO/PORT

CSV/JSON

nodes.csv — node + type/role

edges.csv — src,dst,sport,dport,proto

map.json — nodes, edges, counts

🧪 Getting Sample PCAPs
Wireshark Sample Captures — small, safe protocol demos

Malware-Traffic-Analysis.net — real malware/C2 (handle safely)

NETRESEC PCAPs — curated forensic datasets

Tip: Use curl -L or wget correctly so redirects don’t save HTML as “pcap”.

🛠️ Troubleshooting
Blank white PNG

Means no edges were drawn. Try:

--proto any

Different PCAP (or a longer live capture)

Confirm packets exist: tshark -r file.pcap -c 5

PyShark/TShark errors

Install/upgrade tshark: sudo apt install -y tshark

Keep pcaps off /mnt/c/... to avoid slow I/O in WSL.

Matplotlib GUI errors

We use headless backend (Agg), so PNG saving should work anywhere.

🔮 Roadmap
Per-subnet coloring & communities

Edge thickness by flow volume / bytes

Traceroute/LLDP/SNMP ingestion for true L3 hops (lab environments)

Threat intel enrichment (ASN/GeoIP/hostnames/CVEs)

Interactive HTML graph (pyvis)

📜 License
MIT — see LICENSE.

Author: Zach Lorenz • JCAC 2025 • DNEA-focused portfolio


---

### How to add & push this README

```bash
cd /home/projects/netmap-recon
nano README.md    # paste the content above, save, exit
git add README.md
git commit -m "Add polished README with full CLI usage and examples"
git push -u origin main
