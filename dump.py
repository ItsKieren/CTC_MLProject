from scapy.all import sniff, IP, TCP, UDP, Raw
from collections import defaultdict
import time

connections = defaultdict(lambda: {
    'start_time': None, 'end_time': None,
    'out_bytes': 0, 'in_bytes': 0, 'tot_pkts': 0,
    'state': set()
})

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
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        src_port = packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else None)
        dst_port = packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else None)
        tos = packet[IP].tos
        length = len(packet)

        # Define unique connection key
        connection_key = (src_ip, dst_ip, src_port, dst_port, protocol)
        rev_connection_key = (dst_ip, src_ip, dst_port, src_port, protocol)

        # Determine incoming/outgoing direction
        direction = '->' if connection_key in connections else '<-'

        if connections[connection_key]['start_time'] is None:
            connections[connection_key]['start_time'] = time.time()

        # Update connection end time
        connections[connection_key]['end_time'] = time.time()

        # Update packet and byte counts
        if direction == '->':
            connections[connection_key]['out_bytes'] += length
        else:
            connections[connection_key]['in_bytes'] += length
        connections[connection_key]['tot_pkts'] += 1

        # Track TCP states if applicable
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

        # Calculate duration and rates
        duration = connections[connection_key]['end_time'] - connections[connection_key]['start_time']
        out_bytes = connections[connection_key]['out_bytes']
        in_bytes = connections[connection_key]['in_bytes']
        tot_pkts = connections[connection_key]['tot_pkts']
        tot_bytes = out_bytes + in_bytes
        bytes_per_sec = tot_bytes / duration if duration > 0 else 0
        bytes_per_pkt = tot_bytes / tot_pkts if tot_pkts > 0 else 0
        pkts_per_sec = tot_pkts / duration if duration > 0 else 0
        ratio_out_in = out_bytes / in_bytes if in_bytes > 0 else float('inf')

        # Print details
        print(f"Src IP: {src_ip}, Dst IP: {dst_ip}")
        print(f"Src Port: {src_port} ({port_category(src_port)}), Dst Port: {dst_port} ({port_category(dst_port)})")
        print(f"Proto: {protocol}, ToS: {tos}")
        print(f"Duration: {duration:.2f}s, OutBytes: {out_bytes}, InBytes: {in_bytes}")
        print(f"Total Packets: {tot_pkts}, Total Bytes: {tot_bytes}")
        print(f"Bytes/sec: {bytes_per_sec:.2f}, Bytes/pkt: {bytes_per_pkt:.2f}, Pkts/sec: {pkts_per_sec:.2f}")
        print(f"Ratio Out/In: {ratio_out_in:.2f}")
        print(f"State Flags: {', '.join(connections[connection_key]['state'])}")
        print(f"Direction: {direction}")
        print("-" * 60)

# Start sniffing
sniff(prn=packet_callback, count=10)