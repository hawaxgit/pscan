import asyncio
import argparse
import time
import sys
from ipaddress import ip_network

AUTHOR = "Soroush at Hawax"
SCRIPT_NAME = "Async Portscanner"
VERSION = "3.0"

async def grab_banner(reader, writer):
    """
    Attempts to read initial data (banner) from the open port 
    to identify the software version.
    """
    try:
        # Wait a short moment for the server to send its greeting/banner
        data = await asyncio.wait_for(reader.read(1024), timeout=1.5)
        banner = data.decode('utf-8', errors='ignore').strip().replace('\n', ' ')
        return banner[:60]  # Limit output length to 60 characters
    except (asyncio.TimeoutError, Exception):
        return "No banner received (Silent/No response)"

async def scan_port(ip, port, timeout, semaphore):
    """
    Asynchronously attempts to connect to a specific IP and port.
    """
    async with semaphore:
        try:
            # Attempt to open a connection
            conn = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            
            # If successful, try to identify the service/software
            banner = await grab_banner(reader, writer)
            
            print(f"[+] {ip}:{port:<5} | STATUS: OPEN  | INFO: {banner}")
            
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            # Port is closed, filtered, or unreachable
            return False

async def main_scanner(args):
    """
    Main orchestration logic for the scanning process.
    """
    start_time = time.time()
    
    # Validate and expand the network/IP range
    try:
        net = ip_network(args.ip, strict=False)
        ips = [str(ip) for ip in net]
    except ValueError:
        print(f"[-] Error: Invalid IP address or network range: {args.ip}")
        return

    # Semaphore limits the number of CONCURRENT connections to prevent OS crashes
    semaphore = asyncio.Semaphore(args.max_concurrency)
    
    tasks = []
    print("-" * 75)
    print(f"[*] Scanning {len(ips)} IP(s) for ports {args.start_port} to {args.end_port}...")
    print(f"[*] Concurrency Limit: {args.max_concurrency} parallel requests")
    print("-" * 75 + "\n")

    # Generate scan tasks for all IPs and Ports
    for ip in ips:
        for port in range(args.start_port, args.end_port + 1):
            tasks.append(scan_port(ip, port, args.timeout, semaphore))

    # Execute all tasks concurrently
    await asyncio.gather(*tasks)

    end_time = time.time()
    print("\n" + "-" * 75)
    print(f"{SCRIPT_NAME} {VERSION} completed in {end_time - start_time:.2f} seconds")
    print(f"Author: {AUTHOR} | {WEBSITE}")
    print("-" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Asynchronous Portscanner & Banner Grabber")
    parser.add_argument("ip", help="Target IP or CIDR network (e.g., 192.168.1.1 or 192.168.1.0/24)")
    parser.add_argument("--start-port", type=int, default=1, help="Starting port (Default: 1)")
    parser.add_argument("--end-port", type=int, default=1024, help="Ending port (Default: 1024)")
    parser.add_argument("--timeout", type=float, default=1.5, help="Timeout in seconds (Default: 1.5)")
    parser.add_argument("--max-concurrency", type=int, default=500, help="Max simultaneous connections (Default: 500)")

    args = parser.parse_args()

    # ASCII Header
    print("-" * 75)
    print(f"Welcome to {SCRIPT_NAME} v{VERSION}")
    print(f"Developed by {AUTHOR}")
    print("-" * 75)

    try:
        asyncio.run(main_scanner(args))
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting...")
        sys.exit(0)
