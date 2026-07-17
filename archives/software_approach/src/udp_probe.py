import argparse
import socket


def probe_udp(ip):
    ports = [30050, 3000, 3535, 8888, 9999, 10000, 49152, 49153]
    payloads = [
        b"DAIKIN_UDP/common/basic_info",
        b'{"method":"discover"}',
        b"\x00\x00\x00\x00\x00\x00\x00\x00",
        b"HELLO",
        b"PING",
    ]

    print(f"Probing {ip} with multiple UDP payloads...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    try:
        for port in ports:
            for payload in payloads:
                sock.sendto(payload, (ip, port))
                try:
                    data, addr = sock.recvfrom(1024)
                    print(f"[FOUND RESPONSE] Port {port}: {data.hex()} from {addr[0]}")
                    return
                except socket.timeout:
                    continue
        print("No UDP responses received.")
    finally:
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Authorized target host")
    probe_udp(parser.parse_args().host)
