import asyncio
import argparse
import time
import sys
from ipaddress import ip_network

AUTHOR = "Soroush at Hawax"
SCRIPT_NAME = "Smart Async Portscanner"
VERSION = "3.2"

# Expanded list of the most common 100 ports (for ultra-fast scanning)
# If you want the full Top 1000, we use a range logic below.
COMMON_PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 123, 135, 137, 138, 139, 143, 161, 
    389, 443, 445, 514, 515, 548, 631, 636, 993, 995, 1080, 1433, 1434, 1521, 1701, 1723, 
    2049, 3128, 3306, 3389, 4000, 4848, 5000, 5432, 5632, 5800, 5900, 5985, 6000, 6379, 
    7001, 7077, 8000, 8080, 8081, 8443, 8888, 9000, 9200, 9443, 10000, 27017
]

async def grab_banner(reader, writer):
    """Attempts to identify the software/service version."""
    try:
        # Some services require a small nudge to send a banner
        data = await asyncio.wait_for(reader.read(1024), timeout=1.5)
        banner = data.decode('utf-8', errors='ignore').strip().replace('\n', ' ')
        return banner[:60] if banner else "Connected (No banner/Silent)"
    except:
        return "Unknown Service"

async def scan_port(ip, port, timeout, semaphore):
    """Scans a single port and prints only if it's OPEN."""
    async with semaphore:
        try:
            conn = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            
            # Identify the service
            banner = await grab_banner(reader, writer)
            print(f"[+] {ip:<15} | Port: {port:<5} | Service: {banner}")
            
            writer.close()
            await writer.wait_closed()
        except:
            # Closed or filtered ports are ignored for a clean UI
            pass

async def main_scanner(args):
    start_time = time.time()
    
    try:
        net = ip_network(args.ip, strict=False)
        ips = [str(ip) for ip in net]
    except ValueError:
        print(f"[-] Error: '{args.ip}' is not a valid IP address or CIDR network.")
        return

    # Logic to decide WHICH ports to scan
    if args.all:
        port_list = range(1, 65536)
        mode_label = "Full Scan (1-65535)"
    elif args.top:
        port_list = range(1, 1001)
        mode_label = "Top 1000 Ports"
    else:
        port_list = COMMON_PORTS
        mode_label = "Common Services (Smart Mode)"

    semaphore = asyncio.Semaphore(args.max_concurrency)
    tasks = [scan_port(ip, port, args.timeout, semaphore) for ip in ips for port in port_list]

    print("-" * 75)
    print(f"[*] Starting {SCRIPT_NAME} v{VERSION}")
    print(f"[*] Target(s):  {args.ip} ({len(ips)} IP address(es))")
    print(f"[*] Scan Mode:  {mode_label}")
    print(f"[*] Threads:    {args.max_concurrency} (Concurrent)")
    print("-" * 75 + "\n")

    await asyncio.gather(*tasks)

    duration = time.time() - start_time
    print("\n" + "-" * 75)
    print(f"[*] Scan finished in {duration:.2f} seconds.")
    print(f"[*] Author: {AUTHOR} | {WEBSITE}")
    print("-" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Smart Async Portscanner")
    parser.add_argument("ip", help="Target IP or Network (e.g. 192.168.1.1 or 192.168.1.0/24)")
    parser.add_argument("--all", action="store_true", help="Scan ALL 65535 ports (Slowest)")
    parser.add_argument("--top", action="store_true", help="Scan Top 1000 most common ports")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout (sec)")
    parser.add_argument("--max-concurrency", type=int, default=1000, help="Max parallel tasks")

    try:
        asyncio.run(main_scanner(parser.parse_args()))
    except KeyboardInterrupt:
        print("\n[!] Scan cancelled by user.")
        sys.exit(0)
