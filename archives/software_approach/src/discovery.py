import argparse
import concurrent.futures
import ipaddress
import socket
import urllib.request

def discover_daikin_udp():
    """Finds Daikin units via UDP broadcast on port 30050."""
    print("Searching for Daikin units via UDP...")
    ips = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)

    payloads = [
        b"DAIKIN_UDP/common/basic_info",
        b"DAIKIN_UDP/common/get_model_info",
        b'{"method":"discover"}',
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
    ]

    for msg in payloads:
        print(f"Sending payload: {msg}")
        sock.sendto(msg, ('<broadcast>', 30050))
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print(f"Found: {addr[0]} -> {data.decode('utf-8', errors='ignore')}")
                ips.append(addr[0])
        except socket.timeout:
            pass
    sock.close()
    return list(set(ips))

def scan_ip(ip):
    for port in [80, 8000, 8080]:
        url = f"http://{ip}:{port}/common/basic_info"
        try:
            with urllib.request.urlopen(url, timeout=0.2) as r:
                if r.status == 200:
                    print(f"[FOUND] {ip}:{port}")
                    return f"{ip}:{port}"
        except:
            pass
    return None

def scan_subnet(subnet):
    network = ipaddress.ip_network(subnet, strict=False)
    print(f"Scanning subnet {network}...")
    ips = [str(ip) for ip in network.hosts()]
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(scan_ip, ips)
        for res in results:
            if res:
                found.append(res)
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subnet", help="Authorized subnet, for example 192.0.2.0/24")
    args = parser.parse_args()

    found = discover_daikin_udp()
    if not found and args.subnet:
        found = scan_subnet(args.subnet)

    if found:
        print(f"\nSummary of found units: {found}")
    else:
        print("\nNo Daikin units detected.")
