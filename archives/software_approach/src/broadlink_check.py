import os
import socket


def broadlink_discovery():
    print("Broadlink UDP Discovery (Port 80)...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)

    packet = bytearray(0x30)
    packet[0x26] = 0x06

    sock.sendto(packet, ("<broadcast>", 80))
    target_ip = os.getenv("DAIKIN_AC_IP")
    if target_ip:
        sock.sendto(packet, (target_ip, 80))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Found Device at {addr[0]}")
            print(f"Raw Response: {data.hex()}")
    except socket.timeout:
        print("No response received.")
    finally:
        sock.close()


if __name__ == "__main__":
    broadlink_discovery()
