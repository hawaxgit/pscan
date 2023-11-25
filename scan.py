import argparse
import socket
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_network

AUTHOR = "Soroush Tavanaei at Hawax IT"
SCRIPT_NAME = "Portscanner"
VERSION = "2.0"
WEBSITE = "www.hawax.de"

def signal_handler(sig, frame):
    print('Port scan has ended')
    sys.exit(0)

def validate_ip(ip):
    try:
        ip_network(ip)
        return True
    except ValueError:
        return False

def scan_port(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} open on {ip}")
    except Exception as e:
        print(f"Error scanning port {port} on {ip}: {e}")

def scan(args):
    start_time = time.time()
    signal.signal(signal.SIGINT, signal_handler)

    ips_to_scan = [str(ip) for ip in ip_network(args.ip, strict=False)]

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [executor.submit(scan_port, ip, port, args.timeout) for ip in ips_to_scan for port in range(args.start_port, args.end_port + 1)]

        for _ in as_completed(futures):
            pass

    end_time = time.time()
    print("\n" + "-" * 60)
    print(f"{SCRIPT_NAME} Version {VERSION} completed in {end_time - start_time:.2f} seconds")
    print(f"Autor: {AUTHOR}")
    print(f"Website: {WEBSITE}")
    print("-" * 60)
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portscanner")
    parser.add_argument("ip", help="IP address or network of the target computer")
    parser.add_argument("--start-port", type=int, default=1, help="Start port")
    parser.add_argument("--end-port", type=int, default=65535, help="End port")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout for each socket connection")
    parser.add_argument("--max-workers", type=int, default=200, help="Maximum number of concurrent workers")
    args = parser.parse_args()

    if not validate_ip(args.ip):
        print("Invalid IP address or network.")
        sys.exit(1)

    print("-" * 60)
    print(f"Welcome to {SCRIPT_NAME} Version {VERSION}")
    print(f"Autor: {AUTHOR}")
    print(f"Website: {WEBSITE}")
    print("-" * 60)

    scan(args)
