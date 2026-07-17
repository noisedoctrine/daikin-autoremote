import argparse
import socket
import time


def wake_and_scan(ip):
    print(f"Sending discovery packets to {ip}...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    payloads = [b"DAIKIN_UDP/common/basic_info", b"discovery", b"\x00" * 8]
    for payload in payloads:
        sock.sendto(payload, (ip, 30050))
        sock.sendto(payload, (ip, 3535))
    sock.close()

    time.sleep(1)
    found = False
    for port in [80, 443, 8000, 8080, 8888, 8883, 10000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.5)
            if probe.connect_ex((ip, port)) == 0:
                print(f"Port {port} is OPEN.")
                found = True

    if not found:
        print("No local ports opened.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Authorized target host")
    wake_and_scan(parser.parse_args().host)
