import socket

def tuya_discovery():
    print("Tuya UDP Discovery (Port 6666/6667)...")
    # Tuya uses UDP broadcast for discovery
    for port in [6666, 6667]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(3)
        print(f"Listening on port {port}...")
        try:
            # Tuya devices broadcast periodically, no need to send hello sometimes
            # But let's try to wait for a broadcast
            while True:
                data, addr = sock.recvfrom(1024)
                print(f"Potential Tuya device at {addr[0]}")
                print(f"Data: {data}")
        except socket.timeout:
            print(f"No response on port {port}.")
        finally:
            sock.close()

if __name__ == "__main__":
    tuya_discovery()
