import argparse
import socket
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

AUTHOR = "Hawax"
SCRIPT_NAME = "Portscanner"
VERSION = "1.0"
WEBSITE = "www.hawax.de"

def signal_handler(sig, frame):
    print('Port scan has ended')
    sys.exit(0)

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} open up {ip}")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        pass

def scan(args):
    signal.signal(signal.SIGINT, signal_handler)
    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(scan_port, args.ip, port) for port in range(args.start_port, args.end_port)]

        for _ in as_completed(futures):
            pass

    print("\n" + "-" * 60)
    print(f"{SCRIPT_NAME} Version {VERSION}")
    print(f"Autor: {AUTHOR}")
    print(f"Website: {WEBSITE}")
    print("-" * 60)
    sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Portscanner")
    parser.add_argument("ip", help="IP address of the target computer")
    parser.add_argument("--start-port", type=int, default=1, help="Startport")
    parser.add_argument("--end-port", type=int, default=65535, help="Endport")
    args = parser.parse_args()

    print("-" * 60)
    print(f"Welcome to {SCRIPT_NAME} Version {VERSION}")
    print(f"Autor: {AUTHOR}")
    print(f"Website: {WEBSITE}")
    print("-" * 60)

    scan(args)
