import socket
import sys
import threading
import argparse
from datetime import datetime
from queue import Queue

# --- Globals ---
port_queue = Queue()
open_ports = []
print_lock = threading.Lock() # Prevents threads from writing over each other

# --- Banner Function ---
def print_banner():
    art = r"""
    _                _                   
   / \   _ __   __ _| |_ ___  _ __   __ _ 
  / _ \ | '_ \ / _` | __/ _ \| '_ \ / _` |
 / ___ \| | | | (_| | || (_) | | | | (_| |
/_/   \_\_| |_|\__, |\__\___/|_| |_|\__, |
               |___/                |___/ 
    """
    print(art)
    print("-" * 60)

# --- Argument Parsing ---
def get_arguments():
    parser = argparse.ArgumentParser(description="Angtong Multi-Threaded Port Scanner")
    
    # Positional argument: The target is required
    parser.add_argument("target", help="Target IP address or URL to scan")
    
    # Optional arguments with flags
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    
    return parser.parse_args()

# --- The Job for Each Thread ---
def port_scan(target_ip):
    while not port_queue.empty():
        port = port_queue.get()
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))
            
            if result == 0:
                with print_lock:
                    print(f"[+] Port {port}: OPEN")
                    open_ports.append(port)
            
            s.close()
        except:
            pass
        finally:
            port_queue.task_done()

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Parse Arguments
    args = get_arguments()
    
    target = args.target
    start_port = args.start
    end_port = args.end
    thread_count = args.threads

    print_banner()

    # 2. Resolve Hostname
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"\n[!] Error: Could not resolve hostname '{target}'.")
        sys.exit()

    print(f"Target IP:      {target_ip}")
    print(f"Scanning Ports: {start_port} to {end_port}")
    print(f"Threads:        {thread_count}")
    print(f"Started at:     {datetime.now()}")
    print("-" * 60)

    # 3. Fill Queue
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # 4. Start Threads
    thread_list = []
    # Don't create more threads than actual ports
    actual_threads = min(thread_count, (end_port - start_port + 1))

    for _ in range(actual_threads):
        thread = threading.Thread(target=port_scan, args=(target_ip,))
        thread_list.append(thread)
        thread.start()

    # 5. Wait for threads to finish
    # We wait for the queue to be empty
    port_queue.join() 

    print("-" * 60)
    print(f"Scan completed at: {datetime.now()}")
    
    if open_ports:
        print(f"Summary: Found {len(open_ports)} open ports.")
        print(f"Ports: {sorted(open_ports)}")
    else:
        print("Summary: No open ports found.")
