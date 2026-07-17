import argparse
import os
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = ROOT_DIR / "secrets" / "local.yaml"


def configured_target():
    config_path = Path(os.getenv("DAIKIN_CONFIG", DEFAULT_CONFIG)).expanduser()
    if not config_path.is_absolute():
        config_path = ROOT_DIR / config_path
    if not config_path.exists():
        return None

    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    return config.get("network", {}).get("port_scan_target")


def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        if sock.connect_ex((host, port)) == 0:
            print(f"Port {port} is OPEN")
            return port
    return None


def main():
    parser = argparse.ArgumentParser(description="Scan an authorized local host.")
    parser.add_argument("--host", default=configured_target())
    parser.add_argument("--end-port", type=int, default=10000)
    parser.add_argument("--workers", type=int, default=100)
    args = parser.parse_args()

    if not args.host:
        parser.error("set --host or network.port_scan_target in secrets/local.yaml")
    if not 1 <= args.end_port <= 65535:
        parser.error("--end-port must be between 1 and 65535")
    if not 1 <= args.workers <= 200:
        parser.error("--workers must be between 1 and 200")

    print(f"Scanning {args.host} ports 1-{args.end_port}...")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = executor.map(lambda port: check_port(args.host, port), range(1, args.end_port + 1))
        open_ports = [port for port in results if port]
    print(f"Open ports: {open_ports}")


if __name__ == "__main__":
    main()
