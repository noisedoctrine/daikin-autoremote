import argparse
import subprocess


def run_ps(command):
    try:
        result = subprocess.check_output(
            ["powershell", "-Command", command],
            text=True,
            stderr=subprocess.STDOUT,
        )
        return result.strip()
    except Exception as exc:
        return str(exc)


def discover(ip):
    print(f"Probing {ip} using Windows-native methods...")

    print("\n--- DNS/mDNS Resolution ---")
    print(run_ps(f"Resolve-DnsName {ip} -ErrorAction SilentlyContinue | Select-Object NameHost, Name | Format-Table -HideTableHeaders"))

    print("\n--- NetBIOS Scan (nbtstat) ---")
    try:
        print(subprocess.check_output(["nbtstat", "-A", ip], text=True))
    except Exception:
        print("nbtstat failed or no NetBIOS response.")

    print("\n--- Connection Test (Port 80) ---")
    print(run_ps(f"Test-NetConnection -ComputerName {ip} -Port 80 | Select-Object TcpTestSucceeded"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Authorized target host")
    discover(parser.parse_args().host)
