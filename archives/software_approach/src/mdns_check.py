import socket
import time

def check_mdns():
    print("Checking for all mDNS services on the network...")
    # This is a crude mDNS listener using a raw socket
    # Just to see if ANY device is broadcasting on 5353
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 5353))

    # Join multicast group
    import struct
    mreq = struct.pack("4sl", socket.inet_aton("224.0.0.251"), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock.settimeout(10)
    print("Listening for 10 seconds...")
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"mDNS from {addr[0]}")
    except socket.timeout:
        print("mDNS scan complete.")
    finally:
        sock.close()

if __name__ == "__main__":
    check_mdns()
