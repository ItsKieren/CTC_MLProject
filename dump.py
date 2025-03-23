from flask import Flask, request, redirect, url_for, send_file, render_template
from scapy.all import sniff, IP, TCP, UDP, Raw
from collections import defaultdict
import time
import csv
import threading
import os
from datetime import datetime

app = Flask(__name__, template_folder="templates")

# ----------------------------
# Global Data Structures
# ----------------------------

connections = defaultdict(lambda: {
    'start_time': None,
    'end_time': None,
    'out_bytes': 0,
    'in_bytes': 0,
    'tot_pkts': 0,
    'state': set()
})

# Flag and thread for background capture
capturing = False
capture_thread = None

# ----------------------------
# Helper Functions
# ----------------------------

def port_category(port):
    if port is None:
        return "Unknown"
    if 0 <= port <= 1023:
        return "Well_Known"
    if 1024 <= port <= 49151:
        return "Registered"
    if 49152 <= port <= 65535:
        return "Private"
    return "Unknown"

def packet_callback(packet):
    """This callback function is invoked for each sniffed packet."""
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        
        src_port = packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else None)
        dst_port = packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else None)
        tos = packet[IP].tos
        length = len(packet)
        
        # Unique connection key
        connection_key = (src_ip, dst_ip, src_port, dst_port, protocol)

        # Check direction
        # If the connection_key is new, we treat the first packet as '->'
        direction = '->' if connection_key in connections else '<-'

        # Initialize start_time if first time
        if connections[connection_key]['start_time'] is None:
            connections[connection_key]['start_time'] = time.time()

        # Update end_time
        connections[connection_key]['end_time'] = time.time()

        # Update packet/byte counters
        if direction == '->':
            connections[connection_key]['out_bytes'] += length
        else:
            connections[connection_key]['in_bytes'] += length
        
        connections[connection_key]['tot_pkts'] += 1

        # Track TCP flags if applicable
        if TCP in packet:
            flags = packet.sprintf("%TCP.flags%")
            if "S" in flags:
                connections[connection_key]['state'].add("SYN")
            if "A" in flags:
                connections[connection_key]['state'].add("ACK")
            if "F" in flags:
                connections[connection_key]['state'].add("FIN")
            if "R" in flags:
                connections[connection_key]['state'].add("RST")

def sniff_packets():
    """Repeatedly sniff packets in short intervals while 'capturing' is True."""
    while capturing:
        sniff(prn=packet_callback, timeout=5, store=0)

def save_to_csv(filename="network_traffic.csv"):
    """Save connection data to CSV (same columns/format as original)."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write CSV header
        writer.writerow([
            "Src IP", "Dst IP", "Src Port", "Dst Port", "Protocol", 
            "Duration (s)", "Out Bytes", "In Bytes", "Total Packets",
            "Total Bytes", "Bytes/sec", "Bytes/pkt", "Pkts/sec",
            "Ratio Out/In", "State Flags", "Direction"
        ])

        for (src_ip, dst_ip, src_port, dst_port, protocol), data in connections.items():
            if data['start_time'] is None:
                continue

            duration = data['end_time'] - data['start_time']
            out_bytes = data['out_bytes']
            in_bytes = data['in_bytes']
            tot_pkts = data['tot_pkts']
            tot_bytes = out_bytes + in_bytes

            bytes_per_sec = tot_bytes / duration if duration > 0 else 0
            bytes_per_pkt = tot_bytes / tot_pkts if tot_pkts > 0 else 0
            pkts_per_sec = tot_pkts / duration if duration > 0 else 0
            ratio_out_in = out_bytes / in_bytes if in_bytes > 0 else float('inf')
            state_flags = ', '.join(data['state'])

            writer.writerow([
                src_ip,
                dst_ip,
                src_port,
                dst_port,
                protocol,
                f"{duration:.2f}",
                out_bytes,
                in_bytes,
                tot_pkts,
                tot_bytes,
                f"{bytes_per_sec:.2f}",
                f"{bytes_per_pkt:.2f}",
                f"{pkts_per_sec:.2f}",
                f"{ratio_out_in:.2f}" if ratio_out_in != float('inf') else "inf",
                state_flags,
                "->"
            ])

@app.route("/")
def index():
    """
    Build a 'table_data' list of dicts for each connection,
    doing all float calculations in Python. Pass the
    final (string) values to the template to avoid Jinja float issues.
    """
    table_data = []
    for (src_ip, dst_ip, src_port, dst_port, protocol), data in connections.items():
        if data['start_time'] is None:
            continue
        duration = data['end_time'] - data['start_time']
        out_bytes = data['out_bytes']
        in_bytes = data['in_bytes']
        tot_pkts = data['tot_pkts']
        tot_bytes = out_bytes + in_bytes
        
        if duration > 0:
            bps = tot_bytes / duration
            bpp = tot_bytes / tot_pkts if tot_pkts > 0 else 0
            pps = tot_pkts / duration
        else:
            bps = 0
            bpp = 0
            pps = 0
        
        if in_bytes > 0:
            ratio = out_bytes / in_bytes
        else:
            ratio = float('inf')
        
        state_flags = ", ".join(data['state'])

        # Create a human-readable timestamp from the end_time
        timestamp_str = datetime.fromtimestamp(data['end_time']).strftime('%Y-%m-%d %H:%M:%S')

        table_data.append({
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "protocol": protocol,
            "duration": f"{duration:.2f}",
            "out_bytes": out_bytes,
            "in_bytes": in_bytes,
            "tot_pkts": tot_pkts,
            "tot_bytes": tot_bytes,
            "bytes_per_sec": f"{bps:.2f}",
            "bytes_per_pkt": f"{bpp:.2f}",
            "pkts_per_sec": f"{pps:.2f}",
            "ratio_out_in": f"{ratio:.2f}" if ratio != float('inf') else "inf",
            "state_flags": state_flags,
            "timestamp": timestamp_str
        })

    return render_template("index.html", table_data=table_data, is_capturing=capturing)

@app.route("/start", methods=["POST"])
def start_capture():
    """Start the background sniffing thread (if not already running)."""
    global capturing, capture_thread
    if not capturing:
        capturing = True
        capture_thread = threading.Thread(target=sniff_packets, daemon=True)
        capture_thread.start()
        return {"status": "success", "message": "Capture started"}
    return {"status": "success", "message": "Capture already running"}

@app.route("/stop", methods=["POST"])
def stop_capture():
    """Stop the background sniffing thread and save the CSV."""
    global capturing, connections
    if capturing:
        capturing = False
        filename = f"./scapy_packet_files/network_traffic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_to_csv(filename)  # Save with timestamp in filename
        connections.clear()  # Clear all connections after saving
        # remove files that have already been processed scapy_processed_files
        for file in os.listdir("./scapy_processed_files"):
            os.remove(os.path.join("./scapy_processed_files", file))

        return {"status": "success", "message": f"Capture stopped and saved to {filename}"}
    return {"status": "success", "message": "Capture already stopped"}

@app.route("/download_csv")
def download_csv():
    """Regenerate (or reuse) the CSV file and return it for download."""
    global connections
    filename = "network_traffic.csv"
    save_to_csv(filename)
    connections.clear()  # Clear all connections after saving
    return send_file(filename, as_attachment=True)

@app.route("/get_table_data")
def get_table_data():
    """Return the current table data as JSON for AJAX requests."""
    table_data = []
    for (src_ip, dst_ip, src_port, dst_port, protocol), data in connections.items():
        if data['start_time'] is None:
            continue
        duration = data['end_time'] - data['start_time']
        out_bytes = data['out_bytes']
        in_bytes = data['in_bytes']
        tot_pkts = data['tot_pkts']
        tot_bytes = out_bytes + in_bytes
        
        if duration > 0:
            bps = tot_bytes / duration
            bpp = tot_bytes / tot_pkts if tot_pkts > 0 else 0
            pps = tot_pkts / duration
        else:
            bps = 0
            bpp = 0
            pps = 0
        
        if in_bytes > 0:
            ratio = out_bytes / in_bytes
        else:
            ratio = float('inf')
        
        state_flags = ", ".join(data['state'])
        timestamp_str = datetime.fromtimestamp(data['end_time']).strftime('%Y-%m-%d %H:%M:%S')

        table_data.append({
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "protocol": protocol,
            "duration": f"{duration:.2f}",
            "out_bytes": out_bytes,
            "in_bytes": in_bytes,
            "tot_pkts": tot_pkts,
            "tot_bytes": tot_bytes,
            "bytes_per_sec": f"{bps:.2f}",
            "bytes_per_pkt": f"{bpp:.2f}",
            "pkts_per_sec": f"{pps:.2f}",
            "ratio_out_in": f"{ratio:.2f}" if ratio != float('inf') else "inf",
            "state_flags": state_flags,
            "timestamp": timestamp_str
        })
    return {"table_data": table_data}

@app.route("/get_capture_status")
def get_capture_status():
    """Return the current capture status as JSON."""
    global capturing
    return {"is_capturing": capturing}

# alert route
@app.route("/get_alerts")
def get_alerts():
    """Return the current alerts as JSON."""
    alerts = []
    total_connections = 0
    predicted_alerts = 0
    try:
        for file in os.listdir("scapy_processed_files"):
            if file.endswith(".csv"):
                file_path = os.path.join("scapy_processed_files", file)
                print(f"Processing file: {file_path}")  # Debug log
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        total_connections += 1
                        if row.get('Prediction') == '1':
                            predicted_alerts += 1
                            alerts.append({
                                'src_ip': row.get('Src IP', 'N/A'),
                                'dst_ip': row.get('Dst IP', 'N/A'),
                            })
    except Exception as e:
        print(f"Error processing alerts: {str(e)}")  # Debug log
    
    ratio = predicted_alerts / total_connections if total_connections > 0 else 0
    
    return {
        "alerts": alerts,
        "stats": {
            "total_connections": total_connections,
            "predicted_alerts": predicted_alerts,
            "alert_ratio": ratio
        }
    }

def run_server(host="0.0.0.0", port=8080):
    # Must run with privileges (e.g., 'sudo') to allow Scapy to capture packets
    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    run_server()
