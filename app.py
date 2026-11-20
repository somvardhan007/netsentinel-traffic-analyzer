import threading
import time
from collections import defaultdict, deque
from datetime import datetime
from flask import Flask, jsonify, render_template
from scapy.all import sniff, IP, TCP, UDP, ARP, DNS, DNSQR

app = Flask(__name__)

# Thread-safe state storage
lock = threading.Lock()
stats = {
    "total_packets": 0,
    "total_bytes": 0,
    "protocols": defaultdict(int),
    "top_talkers": defaultdict(int),
    "recent_packets": deque(maxlen=25),
    "alerts": deque(maxlen=20),
    "start_time": time.time()
}

# Anomaly detection state
arp_table = {}  # Maps IP -> MAC to detect ARP spoofing
syn_tracker = defaultdict(set)  # Maps Src_IP -> Set of destination ports
last_syn_reset = time.time()

def log_alert(severity, title, details):
    timestamp = datetime.now().strftime("%H:%M:%S")
    alert_entry = {
        "time": timestamp,
        "severity": severity,
        "title": title,
        "details": details
    }
    # Avoid duplicate consecutive alerts
    if not stats["alerts"] or stats["alerts"][0]["details"] != details:
        stats["alerts"].appendleft(alert_entry)

def analyze_packet(pkt):
    global last_syn_reset
    pkt_len = len(pkt)
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

    with lock:
        stats["total_packets"] += 1
        stats["total_bytes"] += pkt_len

        # Reset SYN port scan tracker every 10 seconds
        if time.time() - last_syn_reset > 10:
            syn_tracker.clear()
            last_syn_reset = time.time()

        # 1. ARP Analysis & Spoofing Detection
        if pkt.haslayer(ARP):
            stats["protocols"]["ARP"] += 1
            if pkt[ARP].op == 2:  # ARP Reply (is-at)
                src_ip = pkt[ARP].psrc
                src_mac = pkt[ARP].hwsrc
                if src_ip in arp_table and arp_table[src_ip] != src_mac:
                    log_alert(
                        "HIGH",
                        "ARP Spoofing Detected",
                        f"IP {src_ip} changed MAC from {arp_table[src_ip]} to {src_mac}"
                    )
                arp_table[src_ip] = src_mac
            return

        # 2. IP Layer Analysis
        if pkt.haslayer(IP):
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            stats["top_talkers"][src_ip] += pkt_len
            proto = "OTHER"
            info = f"{src_ip} -> {dst_ip}"

            # TCP & Port Scan Detection
            if pkt.haslayer(TCP):
                proto = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                flags = pkt[TCP].flags
                info = f"{src_ip}:{sport} -> {dst_ip}:{dport} [Flags: {flags}]"

                if dport in (80, 8080) or sport in (80, 8080):
                    proto = "HTTP"
                elif dport == 443 or sport == 443:
                    proto = "HTTPS"

                # Detect SYN scan (>15 unique ports within 10s)
                if str(flags) == "S":
                    syn_tracker[src_ip].add(dport)
                    if len(syn_tracker[src_ip]) > 15:
                        log_alert(
                            "MEDIUM",
                            "Potential Port Scan (SYN)",
                            f"{src_ip} probed {len(syn_tracker[src_ip])} ports on {dst_ip}"
                        )

            # UDP & DNS Query Inspection
            elif pkt.haslayer(UDP):
                proto = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
                info = f"{src_ip}:{sport} -> {dst_ip}:{dport}"

                if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
                    proto = "DNS"
                    qname = pkt[DNSQR].qname.decode("utf-8", errors="ignore").rstrip(".")
                    info = f"DNS Query: {qname} ({src_ip})"

            stats["protocols"][proto] += 1
            stats["recent_packets"].appendleft({
                "time": timestamp,
                "src": src_ip,
                "dst": dst_ip,
                "proto": proto,
                "len": pkt_len,
                "info": info
            })

def sniff_interface(iface_name):
    # store=0 keeps memory bounded; iface filters traffic to one interface per thread
    sniff(iface=iface_name, prn=analyze_packet, store=0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def get_stats():
    with lock:
        uptime = max(1, int(time.time() - stats["start_time"]))
        sorted_talkers = sorted(
            stats["top_talkers"].items(), key=lambda x: x[1], reverse=True
        )[:5]

        return jsonify({
            "total_packets": stats["total_packets"],
            "total_kb": round(stats["total_bytes"] / 1024, 2),
            "pps": round(stats["total_packets"] / uptime, 1),
            "protocols": dict(stats["protocols"]),
            "top_talkers": [{"ip": ip, "kb": round(b / 1024, 2)} for ip, b in sorted_talkers],
            "recent_packets": list(stats["recent_packets"]),
            "alerts": list(stats["alerts"])
        })


if __name__ == "__main__":
    interfaces = ["lo", "wlo1"]  # Replace "wlan0" with your active interface from `ip route`
    for iface in interfaces:
        t = threading.Thread(target=sniff_interface, args=(iface,), daemon=True)
        t.start()

    print("[*] Starting Web Dashboard on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
x
